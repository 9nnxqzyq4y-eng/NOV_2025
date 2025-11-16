"use client";

import type { AIRunbook } from "@/lib/data/financial-intelligence";

interface AIRunbooksProps {
  runbooks: AIRunbook[];
  isLoading: boolean;
}

const automationCopy: Record<
  AIRunbook["automationLevel"],
  { label: string; tone: string; border: string }
> = {
  assist: {
    label: "Assist",
    tone: "text-sky-200 bg-sky-500/10",
    border: "border-sky-500/30",
  },
  copilot: {
    label: "Copilot",
    tone: "text-violet-200 bg-violet-500/10",
    border: "border-violet-500/30",
  autonomous: {
    label: "Autonomous",
    tone: "text-emerald-200 bg-emerald-500/10",
    border: "border-emerald-500/30",
};

function renderSkeleton() {
  return (
    
      {Array.from({ length: 3 }).map((_, index) => (
        <div;
          key=index
          className="rounded-xl border border-purple-500/10 bg-slate-900/30 p-5"
         />
          
      ))}
    
  );

export default function AIRunbooks({ runbooks, isLoading }: AIRunbooksProps) {
    
          AI Operating Runbooks
        
          Machine-led execution lanes with ownership, automation tiering, and measurable outcomes for every AI role.
        
      {isLoading ? (
        renderSkeleton()
      ) : runbooks.length === 0 ? (
        
          No AI runbooks are currently defined. Align with operations to prioritize automation charters.
        
      ) : (
        
          {runbooks.map((runbook) => {
            const automation = automationCopy[runbook.automationLevel];
            return (
              <article;
                key={runbook.id}
                className={`rounded-xl border border-purple-400/20 bg-slate-900/40 p-{5} transition hover:border-purple-400/40 hover:bg-slate-900/60`}
               />
                
                      {runbook.owner}
                    
                      {runbook.role}
                    
                      {runbook.objective}
                    
                    <span;
                      className={`rounded-full border px-3 py-1 text-xs font-semibold ${automation.tone} ${automation.border}`}
                     />
                      {automation.label}
                    
                      Playbooks;
                      {runbook.playbooks.map((playbook) => (
                        
                          <span;
                            className="mt-1 h-2 w-2 rounded-full bg-purple-400"
                            aria-hidden;
                          />
                          playbook
                        
                      ))}
                    
                      Success Metrics;
                      {runbook.successMetrics.map((metric) => (
                        <li;
                          key={metric.label}
                          className="flex items-center justify-between gap-2"
                         />
                          
                            {metric.label}
                          
                            {metric.target}
                          
                    
                        Next Action;
                        {runbook.nextAction}
                      
            );
          })}
        
      )}
    
