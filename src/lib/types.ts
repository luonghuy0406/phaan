// Shape of public/cases/<id>/case.json. See docs/case-schema.md.

export type DocType = 'newspaper' | 'report' | 'testimony' | 'photo' | 'letter' | 'receipt' | 'evidence' | 'note' | 'scan' | 'people';

export interface Field { label: string; value: string }

export interface CaseDoc {
  id: string;
  /** type "people": filled from the case's victim + suspects when the case loads */
  persons?: (CasePerson & { victim?: boolean })[];
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
  /** free text in light Markdown: blank line = new paragraph, "- " / "1. " lists, **bold** (see docs/case-schema.md) */
  content?: string;
  paragraphs?: string[];
  header?: string[];
  heading?: string;
  code?: string;
  fields?: Field[];
  sections?: { heading: string; paragraphs: string[] }[];
  signature?: string;
  /** signature blocks at the foot of official papers, e.g. [{ role: "Điều tra viên", name: "Vũ Minh Tâm" }] */
  signers?: { role: string; name: string }[];
  /** form number printed top-right, e.g. "Mẫu số 138" */
  form?: string;
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
  /** each point is { title, body[] }; a plain string is accepted too */
  explanation?: ({ title: string; body: string[] } | string)[];
  /** choice shown as suspect ID cards: suspect id for each option, same order as `options` */
  cards?: string[];
  /** conclusion reported to an AI prosecutor (rubric on the server, authoring/<id>/conclusion.json); the choice stays as the fallback */
  exam?: { examiner: string; intro?: string };
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
  /** 'fiction' (made-up people and places) or 'true-crime' (reconstructed from a real case) */
  kind?: CaseKind;
  /** content is playable but images are still being made: shown with a "Chưa hoàn thiện" label */
  draft?: boolean;
}

export type CaseKind = 'fiction' | 'true-crime';

export interface CaseData extends CaseSummary {
  subtitle?: string;
  era?: string;
  contentWarning?: string;
  /** print "Cộng hòa xã hội chủ nghĩa Việt Nam" on official papers (default true; false for cases set abroad) */
  nationalHeader?: boolean;
  synopsis?: string[];
  intro?: { title?: string; paragraphs?: string[]; objective?: string };
  documents: CaseDoc[];
  questions: Question[];
  finale?: { title?: string; paragraphs?: string[] };
  epilogue?: { title: string; text: string }[];
  tour?: { title: string; text: string }[];
  /** short scene shown when a round opens (stage ≥ 2), with an optional narration clip */
  beats?: CaseBeat[];
  /** case audio, paths relative to the case folder: looped ambience and narration for intro / finale */
  audio?: { ambient?: string; intro?: string; finale?: string };
  /** people of the case shown as ID cards (intro, "Nghi phạm" dialog, card questions) */
  suspects?: CasePerson[];
  victim?: CasePerson;
  /** suspects can be questioned by AI (server profile synced from authoring/<id>/interrogation.json) */
  aiInterrogation?: boolean;
}

export interface CasePerson { id: string; name: string; alias?: string; age?: number; role?: string; image?: string; suspicion?: string; note?: string; /** on-device voice (Supertonic F1–F5, M1–M5) for interrogation replies */ voice?: string }

export interface CaseBeat { stage: number; kicker?: string; title?: string; paragraphs: string[]; voice?: string }

export type CheckStatus = 'correct' | 'near' | 'wrong' | 'incomplete';
export interface CheckResult { status: CheckStatus; message: string }
