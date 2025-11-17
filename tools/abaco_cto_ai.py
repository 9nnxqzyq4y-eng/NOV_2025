#!/usr/bin/env python3
import ast
import re
import json
import logging
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GATING_THRESHOLD = 2.0
TOOL_VERSION = "3.0.0"
HIGH_CONFIDENCE = 0.9
MEDIUM_CONFIDENCE = 0.7
LOW_CONFIDENCE = 0.5

@dataclass
class AnalysisResult:
    agent_id: str
    timestamp: datetime
    findings: List[Dict[str, Any]]
    file_path: str
    confidence_score: float
    metadata: Dict[str, Any]

class AbacoCodeAnalyzer:
    def __init__(self, agent_id: str, config_path: Optional[str] = None):
        self.agent_id = agent_id
        self.config = self._load_config(config_path) if config_path else {}
        
        self.llm_patterns = [
            re.compile(r'openai\.(?:ChatCompletion|chat\.completions)\.create', re.IGNORECASE),
            re.compile(r'anthropic\.(?:Client|messages)\.create', re.IGNORECASE),
            re.compile(r'google\.generativeai\.generate_text', re.IGNORECASE),
            re.compile(r'gemini\.(?:generate|chat)', re.IGNORECASE),
        ]
        
        self.gating_patterns = [
            re.compile(r'rate_limit|throttle|quota|budget|circuit_breaker', re.IGNORECASE),
            re.compile(r'retry|backoff|timeout', re.IGNORECASE),
            re.compile(r'try\s*:.*except', re.MULTILINE),
            re.compile(r'@.*(?:limit|throttle|rate)', re.IGNORECASE),
            re.compile(r'if\s+.*(?:cost|limit|budget)', re.IGNORECASE),
        ]

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.warning(f"Failed to load config from {config_path}: {e}")
            return {}

    def detect_llm_usage_without_gating(self, source: str, file_path: str) -> List[Dict[str, Any]]:
        findings = []
        lines = source.splitlines()
        
        for line_num, line in enumerate(lines, 1):
            for pattern in self.llm_patterns:
                if pattern.search(line):
                    context_start = max(0, line_num - 10)
                    context_end = min(len(lines), line_num + 10)
                    context = '\n'.join(lines[context_start:context_end])
                    
                    gating_score = 0
                    gating_evidence = []
                    
                    for gating_pattern in self.gating_patterns:
                        matches = gating_pattern.findall(context)
                        if matches:
                            gating_score += len(matches)
                            gating_evidence.extend(matches)
                    
                    has_sufficient_gating = gating_score >= GATING_THRESHOLD
                    
                    if not has_sufficient_gating:
                        confidence = HIGH_CONFIDENCE if 'api_key' in line.lower() else MEDIUM_CONFIDENCE
                        if gating_score > 0:
                            confidence = MEDIUM_CONFIDENCE
                        
                        findings.append({
                            'type': 'llm_without_sufficient_gating',
                            'severity': 'critical' if gating_score == 0 else 'high',
                            'line': line_num,
                            'file': file_path,
                            'message': f'LLM API call with insufficient gating (score: {gating_score}/{GATING_THRESHOLD})',
                            'gating_score': gating_score,
                            'gating_evidence': gating_evidence,
                            'confidence': confidence,
                            'recommendation': 'Add rate limiting, circuit breakers, and error handling'
                        })
                    break
        
        return findings

    def detect_silent_failures(self, source: str, file_path: str) -> List[Dict[str, Any]]:
        findings = []
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            return [{
                'type': 'syntax_error',
                'severity': 'critical',
                'line': e.lineno or 0,
                'file': file_path,
                'message': f'Syntax error prevents analysis: {e.msg}',
                'confidence': 1.0
            }]
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                is_bare = node.type is None
                is_broad = (isinstance(node.type, ast.Name) and 
                           node.type.id in ['Exception', 'BaseException'])
                is_silent = (len(node.body) == 1 and 
                           isinstance(node.body[0], (ast.Pass, ast.Ellipsis))) or len(node.body) == 0
                
                if (is_bare or is_broad) and is_silent:
                    findings.append({
                        'type': 'silent_failure',
                        'severity': 'critical',
                        'line': node.lineno,
                        'file': file_path,
                        'message': 'Silent failure: broad exception with no handling',
                        'confidence': HIGH_CONFIDENCE,
                        'recommendation': 'Add logging and specific exception handling'
                    })
        
        return findings

    def analyze_file(self, file_path: str) -> AnalysisResult:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='strict') as f:
                source = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    source = f.read()
                logger.warning(f"File {file_path} read with latin-1 encoding")
            except Exception as e:
                return AnalysisResult(
                    agent_id=self.agent_id,
                    timestamp=datetime.now(),
                    findings=[{
                        'type': 'file_read_error',
                        'message': f'Cannot read file: {e}',
                        'confidence': 1.0
                    }],
                    file_path=file_path,
                    confidence_score=0.0,
                    metadata={'error': str(e)}
                )
        
        if not source.strip():
            return AnalysisResult(
                agent_id=self.agent_id,
                timestamp=datetime.now(),
                findings=[],
                file_path=file_path,
                confidence_score=1.0,
                metadata={'status': 'empty_file'}
            )
        
        findings = []
        findings.extend(self.detect_llm_usage_without_gating(source, file_path))
        findings.extend(self.detect_silent_failures(source, file_path))
        
        if not findings:
            confidence = 1.0
        else:
            confidence = sum(f.get('confidence', LOW_CONFIDENCE) for f in findings) / len(findings)
        
        return AnalysisResult(
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            findings=findings,
            file_path=file_path,
            confidence_score=confidence,
            metadata={
                'tool_version': TOOL_VERSION,
                'analysis_timestamp': datetime.now().isoformat(),
                'gating_threshold': GATING_THRESHOLD
            }
        )

    def save_results(self, results: List[AnalysisResult], output_path: str) -> None:
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            output_data = {
                'metadata': {
                    'tool_version': TOOL_VERSION,
                    'timestamp': datetime.now().isoformat(),
                    'agent_id': self.agent_id,
                    'files_analyzed': len(results),
                    'gating_threshold': GATING_THRESHOLD
                },
                'results': [
                    {
                        'file_path': r.file_path,
                        'confidence_score': r.confidence_score,
                        'findings_count': len(r.findings),
                        'findings': r.findings,
                        'metadata': r.metadata
                    }
                    for r in results
                ]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
                
        except (OSError, IOError) as e:
            logger.error(f"Failed to save results to {output_path}: {e}")
            raise

def main() -> int:
    import argparse
    
    parser = argparse.ArgumentParser(description='ABACO CTO AI Code Analysis Tool')
    parser.add_argument('files', nargs='*', help='Files to analyze')
    parser.add_argument('--output', '-o', help='Output file for results')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--agent-id', default='abaco_cto_agent', help='Agent identifier')
    
    args = parser.parse_args()
    
    if not args.files:
        logger.error("No files specified for analysis")
        return 1
    
    analyzer = AbacoCodeAnalyzer(args.agent_id, args.config)
    results = []
    
    for file_path in args.files:
        if not os.path.exists(file_path):
            logger.warning(f"File not found: {file_path}")
            continue
        result = analyzer.analyze_file(file_path)
        results.append(result)
    
    if args.output:
        analyzer.save_results(results, args.output)
    else:
        total_findings = sum(len(r.findings) for r in results)
        print(f"Analysis complete: {len(results)} files, {total_findings} findings")
    
    return 0

if __name__ == "__main__":
    exit(main())
