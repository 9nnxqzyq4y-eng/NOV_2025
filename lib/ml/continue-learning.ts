import { createClient } from '@/lib/supabase/server';
import type { ModelMetrics, Prediction } from './types';

export class ContinueLearning {
  /** Save a new prediction – returns the record id */
  static async recordPrediction(pred: OmitPrediction, 'id' | 'createdAt' | 'status'): Promisestring {
    const supabase  await createClient();

    const { data, error }  await supabase
      .from('ml_predictions')
      .insert([{
        model_id: pred.modelId,
        customer_id: pred.customerId,
        metric: pred.metric,
        predicted_value: pred.predictedValue,
        confidence: pred.confidence,
        reasoning: pred.reasoning,
        status: 'awaiting_feedback',
      }])
      .select('id')
      .single();

    if (error) throw new Error(error.message);
    return data.id;
  }

  /** Submit feedback – updates the row and recalculates model metrics */
  static async submitFeedback(
    predictionId: string,
    actual: number,
    userFeedback?: string
  ): Promise{ accuracy: number } {
    const supabase  await createClient();

    // Fetch prediction
    const { data: pred, error: fetchErr }  await supabase
      .from('ml_predictions')
      .select('*')
      .eq('id', predictionId)
      .single();

    if (fetchErr) throw new Error(fetchErr.message);

    const errorMag  Math.abs(actual - pred.predicted_value);
    const wasCorrect  errorMag  0.1 * pred.predicted_value; // 10% tolerance
    const errorType  actual  pred.predicted_value ? 'underestimate' : 'overestimate';

    // Update prediction
    await supabase
      .from('ml_predictions')
      .update({
        actual_outcome: actual,
        was_correct: wasCorrect,
        error_magnitude: errorMag,
        error_type: errorType,
        user_feedback: userFeedback,
        feedback_at: new Date().toISOString(),
        status: 'feedback_received',
      })
      .eq('id', predictionId);

    // Recalc model metrics
    const { data: all, error: metricErr }  await supabase
      .from('ml_predictions')
      .select('was_correct')
      .eq('model_id', pred.model_id)
      .eq('status', 'feedback_received');

    if (metricErr) throw new Error(metricErr.message);

    const correct  all.filter(r  r.was_correct).length;
    const total  all.length;
    const accuracy  total ? (correct / total) * 100 : 0;

    await supabase
      .from('ml_model_metrics')
      .upsert({
        model_id: pred.model_id,
        total_predictions: total,
        correct_predictions: correct,
        accuracy,
        last_updated: new Date().toISOString(),
      });

    return { accuracy };
  }

  /** Get current metrics for a model */
  static async getMetrics(modelId: string): PromiseModelMetrics {
    const supabase  await createClient();
    const { data, error }  await supabase
      .from('ml_model_metrics')
      .select('*')
      .eq('model_id', modelId)
      .single();

    if (error && error.code  'PGRST116') {
      // No row yet
      return {
        modelId,
        totalPredictions: 0,
        correctPredictions: 0,
        accuracy: 0,
        lastUpdated: new Date().toISOString()
      };
    }
    if (error) throw new Error(error.message);
    return data;
  }
}
