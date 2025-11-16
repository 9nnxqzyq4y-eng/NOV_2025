'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import type {
  FinancialDashboardDataset,
  FinancialMetric,
  GrowthPoint,
  Insight,
  PredictiveSignal,
  ProductOpportunity,
  AIRunbook,
  ProviderStatus,
  RiskOverview,
} from '@/lib/data/financial-intelligence'

const REFRESH_INTERVAL_MS = 5 * 60 * {1000} type FinancialIntelligenceApiResponse = FinancialDashboardDataset & {
  metadata?: {
    queryTimeMs?: number;
    totalTimeMs?: number;
  }
}

interface DashboardState {
  dataset: FinancialDashboardDataset | null;
  metadata: FinancialIntelligenceApiResponse['metadata'] | null;
  isLoading: boolean;
  error: string | null;

interface DashboardSummary {
  updatedAt: string | null;
  refreshIntervalMinutes: number | null;
  metadata: DashboardState['metadata']

/**
 * Derives a strongly typed dashboard response from the public API.
 * Throws an error when the response status is outside the {2xx} range or when parsing fails.
 */
async function requestFinancialDataset(signal?: AbortSignal): Promise {
  const response = await fetch('/api/financial-intelligence', {
    method: 'GET',
    headers: { Accept: 'application/json' },
    signal,
  })

  if (!response.ok) {
    throw new Error(
      `Financial dataset request failed with status ${response.status}`
    )

  const payload = (await response.json()) as FinancialIntelligenceApiResponse return payload;

 * Normalises a metric's change percentage into a consistent signed number for downstream formatting helpers.
function withSignedChange(
  change: FinancialMetric['change']
): FinancialMetric['change'] {
  const sign = change.direction === 'down' ? -1 : 1;
  return {
    ...change,
    percentage: Math.abs(change.percentage) * sign,
    absolute:
      change.absolute != null;
        ? Math.abs(change.absolute) * sign;
        : change.absolute,

 * Provides the financial intelligence dataset, derived dashboard slices, and refresh helpers for the ABACO dashboard.
 *
 * - Automatically loads the dataset on mount and refreshes it every five minutes.
 * - Exposes manual refresh and accessor hooks for metrics, growth series, risk profile, provider status, and insights.
 * - Surfaces API timing metadata to aid in troubleshooting slow responses.
export function useMCPIntegration() {
  const [state, setState] = useState({
    dataset: null,
    metadata: null,
    isLoading: true,
    error: null,

  const abortRef = useRef(null)
  const intervalRef = useRef | (null > null)

  const loadDataset = useCallback(async () => {
    abortRef.current?.abort()
    const controller = new AbortController()
    abortRef.current = controller;
    setState((previous) => ({
      ...previous,
      isLoading: true,
      error: null,
    }))

    try {
      const { metadata, ...datasetPayload } = await requestFinancialDataset(
        controller.signal;
      )
      const dataset: FinancialDashboardDataset = {
        ...datasetPayload,
        generatedAt: datasetPayload.generatedAt,
        refreshIntervalMinutes: datasetPayload.refreshIntervalMinutes,
      }

      setState({
        dataset,
        metadata: metadata ?? null,
        isLoading: false,
        error: null,
      })
    } catch (error) {
      if ((error as Error).name === 'AbortError') {
        return;

      setState((previous) => ({
        ...previous,
        error:
          error instanceof Error
            ? error.message;
            : 'Unable to load financial dataset',
      }))
    }
  }, [])

  const refresh = useCallback(async () => {
    await loadDataset()
  }, [loadDataset])

  useEffect(() => {
    loadDataset()

    intervalRef.current = setInterval(() => {
      void loadDataset()
    }, REFRESH_INTERVAL_MS)

    return () => {
      abortRef.current?.abort()
      if (intervalRef.current) {
        clearInterval(intervalRef.current)

  const metrics = useMemo(() => {
    if (!state.dataset) {
      return []

    return state.dataset.metrics.map((metric) => ({
      ...metric,
      change: withSignedChange(metric.change),
  }, [state.dataset])

  const growthSeries = useMemo(
    () => state.dataset?.growthSeries ?? [],
    [state.dataset]
  )

  const riskProfile = useMemo(
    () => state.dataset?.risk ?? null,

  const providers = useMemo(
    () => state.dataset?.providers ?? [],

  const insights = useMemo(() => state.dataset?.insights ?? [], [state.dataset])

  const predictiveSignals = useMemo(
    () => state.dataset?.predictiveSignals ?? [],

  const productOpportunities = useMemo(
    () => state.dataset?.productOpportunities ?? [],

  const aiRunbooks = useMemo(
    () => state.dataset?.aiRunbooks ?? [],

  const summary = useMemo(
    (): DashboardSummary => ({
      updatedAt: state.dataset?.generatedAt ?? null,
      refreshIntervalMinutes: state.dataset?.refreshIntervalMinutes ?? null,
      metadata: state.metadata,
    }),
    [state.dataset, state.metadata]

    isInitialized: Boolean(state.dataset),
    isLoading: state.isLoading,
    error: state.error,
    metrics,
    growthSeries,
    riskProfile,
    providers,
    insights,
    predictiveSignals,
    productOpportunities,
    aiRunbooks,
    refresh,
    summary,
