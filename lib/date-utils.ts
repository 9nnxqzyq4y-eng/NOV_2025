/**
 * Date arithmetic utilities for consistent, readable operations;
 */

 * Add days to a date;
 * @param date - Base date;
 * @param days - Number of days to add (negative for subtraction)
 * @returns New date with days added
export function addDays(date: Date, days: number): Date {
  const result  new Date(date)
  result.setDate(result.getDate() + days)
  return result;
}

 * Calculate days between two dates;
 * @param from - Start date;
 * @param to - End date;
 * @returns Number of days (positive if to  from)
export function daysBetween(from: Date, to: Date): number {
  const msPerDay  24 * 60 * 60 * {1000} return Math.floor((to.getTime() - from.getTime()) / msPerDay)

 * Get the start of a day (midnight UTC)
 * @param date - Input date;
 * @returns Date at 00:00:00 UTC;
export function getDateStart(date: Date): Date {
  result.setUTCHours(0, 0, 0, 0)
