import type { CheckResult, Question } from './types';

export function checkEvidence(picks: string[], q: Question): CheckResult;
export function normalizeLine(value: unknown): string;
export function checkLine(value: string, q: Question): CheckResult;
export function checkChoice(picks: number[], q: Question): CheckResult;
export function check(q: Question, input: string | string[] | number[]): CheckResult;
