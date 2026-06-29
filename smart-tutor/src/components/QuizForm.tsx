import { useState } from "react";

export interface Question {
  id: number;
  text: string;
  options: string[];
}

interface QuizFormProps {
  questions: Question[];
  onSubmit: (answers: Record<number, number>) => void;
  loadingGrading: boolean;
}

export default function QuizForm({ questions, onSubmit, loadingGrading }: QuizFormProps) {
  const [responses, setResponses] = useState<Record<number, number>>({});

  const handleSelect = (qid: number, idx: number) => {
    setResponses({ ...responses, [qid]: idx });
  };

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(responses);
  };

  return (
    <form onSubmit={handleFormSubmit} className="space-y-6">
      {questions.map((q) => (
        <div key={q.id} className="bg-[#0e1122]/40 border border-zinc-800/40 p-6 rounded-xl shadow-md space-y-4">
          <p className="font-bold text-zinc-100 leading-relaxed">{q.text}</p>
          <div className="space-y-3.5">
            {q.options.map((opt, idx) => {
              const isSelected = responses[q.id] === idx;
              return (
                <label
                  key={idx}
                  className={`flex items-center space-x-3.5 p-4 rounded-xl border cursor-pointer transition duration-150 ${
                    isSelected
                      ? "border-cyan-500/50 bg-cyan-500/10 text-cyan-300"
                      : "border-zinc-850 bg-zinc-950/20 text-zinc-300 hover:bg-zinc-800/20"
                  }`}
                >
                  <input
                    type="radio"
                    name={`q-${q.id}`}
                    checked={isSelected}
                    onChange={() => handleSelect(q.id, idx)}
                    className="w-4 h-4 text-cyan-500 focus:ring-cyan-500/20 bg-zinc-900 border-zinc-800"
                  />
                  <span className="text-sm font-medium">{opt}</span>
                </label>
              );
            })}
          </div>
        </div>
      ))}
      <div className="flex justify-end pt-4">
        <button
          type="submit"
          disabled={loadingGrading || Object.keys(responses).length < questions.length}
          className="w-full md:w-auto px-8 py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 disabled:from-zinc-800 disabled:to-zinc-800 text-white font-bold rounded-xl transition duration-200 shadow-[0_0_15px_rgba(6,182,212,0.2)] hover:shadow-[0_0_25px_rgba(6,182,212,0.4)] disabled:shadow-none cursor-pointer disabled:cursor-not-allowed text-sm"
        >
          {loadingGrading ? "Evaluating answers..." : "Submit Answers"}
        </button>
      </div>
    </form>
  );
}
