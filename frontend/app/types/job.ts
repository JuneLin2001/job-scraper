export type JobSource = "104" | "1111";

export interface Job {
  id: number;
  title: string;
  description: string;
  salary: string;
  company_name: string;
  location: string;
  source: JobSource[];
  links: string[];
  labels: string[];
  updated_at: string;
}
