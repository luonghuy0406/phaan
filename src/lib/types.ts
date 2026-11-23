// Shape of public/cases/<id>/case.json. See docs/case-schema.md.

export type DocType = 'newspaper' | 'report' | 'testimony' | 'photo' | 'letter' | 'receipt' | 'evidence' | 'note' | 'scan';

export interface Field { label: string; value: string }

export interface CaseDoc {
  id: string;
  stage?: number;
  no?: number;
  type: DocType;
  title: string;
  x?: number;
  y?: number;
  width?: number;
  rotate?: number;
  // type specific (all optional; renderers read what they need)
  masthead?: string;
  issue?: string;
  date?: string;
  headline?: string;
  deck?: string;
  image?: string | null;
  imageHi?: string;      // sharper file, loaded when the paper is zoomed in
  file?: string;         // original file players can download (PDF / image)
  imageCaption?: string;
  paragraphs?: string[];
  header?: string[];
  heading?: string;
  code?: string;
  fields?: Field[];
  sections?: { heading: string; paragraphs: string[] }[];
  signature?: string;
  lines?: { n: number; text: string; speaker?: string }[];
  caption?: string;
  label?: string;
  greeting?: string;
  shop?: string;
  address?: string;
  items?: { name: string; qty?: string; price?: string }[];
  total?: string;
  footer?: string[];
}

export interface Nudge { picks?: string[]; any?: string[]; near?: boolean; message: string }
export interface MapNudge { near?: boolean; message: string }

export interface Question {
  id: string;
  stage?: number;
  type: 'evidence' | 'line' | 'choice';
  title: string;
  prompt?: string | string[];
  need?: number;
  answer?: (string | number)[];
  options?: string[];
  multiple?: boolean;
  nudges?: Nudge[] | Record<string, MapNudge>;
  hints?: string[];
  solved?: string;
  wrong?: string;
  incomplete?: string;
  submit?: string;
  explanation?: { title: string; body: string[] }[];
}

export interface CaseSummary {
  id: string;
  no: number;
  status: 'available' | 'coming-soon';
  title: string;
  tagline?: string;
  difficulty?: number;
  players?: string;
  duration?: string;
  setting?: string;
  tags?: string[];
  cover?: string | null;
}

export interface CaseData extends CaseSummary {
  subtitle?: string;
  era?: string;
  contentWarning?: string;
  synopsis?: string[];
  intro?: { title?: string; paragraphs?: string[]; objective?: string };
  documents: CaseDoc[];
  questions: Question[];
  finale?: { title?: string; paragraphs?: string[] };
  epilogue?: { title: string; text: string }[];
  tour?: { title: string; text: string }[];
}

export type CheckStatus = 'correct' | 'near' | 'wrong' | 'incomplete';
export interface CheckResult { status: CheckStatus; message: string }
