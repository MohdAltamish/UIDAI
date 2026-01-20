
export interface EnrollmentData {
  state: string;
  enrollments: number;
  male: number;
  female: number;
  transgender: number;
  ageGroups: {
    "0-18": number;
    "19-35": number;
    "36-60": number;
    "60+": number;
  };
}

export interface ScriptInsight {
  id: string;
  name: string;
  description: string;
  pythonFile: string;
  type: 'bar' | 'scatter' | 'heatmap' | 'line' | 'pie';
}

export interface AIAnalysis {
  summary: string;
  insights: string[];
  recommendations: string[];
}
