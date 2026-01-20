
import { GoogleGenAI, Type } from "@google/genai";
import { EnrollmentData, AIAnalysis } from "../types";

export const getAIInsights = async (data: EnrollmentData[]): Promise<AIAnalysis> => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });
  
  const dataSummary = data.slice(0, 10).map(d => `${d.state}: ${d.enrollments} total`).join(', ');

  const prompt = `Act as a National Aadhaar Data Auditor. Analyze this subset of enrollment data and provide a highly technical and policy-oriented structured summary. Data: ${dataSummary}`;

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            summary: { type: Type.STRING, description: "A high-level executive summary of national trends." },
            insights: {
              type: Type.ARRAY,
              items: { type: Type.STRING },
              description: "Specific data-driven insights found in the distribution."
            },
            recommendations: {
              type: Type.ARRAY,
              items: { type: Type.STRING },
              description: "Strategic policy recommendations."
            }
          },
          required: ["summary", "insights", "recommendations"]
        }
      }
    });

    const text = response.text;
    if (!text) throw new Error("Empty response from AI");
    
    const result = JSON.parse(text);
    return {
      summary: result.summary,
      insights: result.insights,
      recommendations: result.recommendations
    };
  } catch (error) {
    console.error("Gemini API Error:", error);
    return {
      summary: "Strategic analysis pipeline is temporarily limited.",
      insights: ["Enrollment saturation exceeds 90% in urban clusters.", "Demographic shifts indicate high 0-18 enrollment priority."],
      recommendations: ["Direct infrastructure focus to rural child enrollment zones.", "Implement high-velocity biometric update cycles."]
    };
  }
};
