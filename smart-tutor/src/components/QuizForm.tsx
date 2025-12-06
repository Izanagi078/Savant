// components/QuizForm.tsx
import { useState } from "react";

interface Question {
  id: number;
  text: string;
  options: string[];
  answer: number; // index of correct option
}

const sampleQuestions: Question[] = [
  {
    id: 1,
    text: "What is 2 + 2?",
    options: ["3", "4", "5"],
    answer: 1,
  },
  {
    id: 2,
    text: "Capital of France?",
    options: ["Berlin", "Madrid", "Paris"],
    answer: 2,
  },
];

export default function QuizForm() {
  const [responses, setResponses] = useState<Record<number, number>>({});
  const [submitted, setSubmitted] = useState(false);

  const handleSelect = (qid: number, idx: number) => {
    setResponses({ ...responses, [qid]: idx });
  };

  const handleSubmit = () => {
    setSubmitted(true);
  };

  return (
    <div className="p-4 border rounded-lg shadow-md bg-white">
      <h2 className="text-xl font-bold mb-4">Quiz</h2>
      {sampleQuestions.map((q) => (
        <div key={q.id} className="mb-4">
          <p className="font-medium">{q.text}</p>
          <div className="space-y-2 mt-2">
            {q.options.map((opt, idx) => (
              <label
                key={idx}
                className="flex items-center space-x-2 cursor-pointer"
              >
                <input
                  type="radio"
                  name={`q-${q.id}`}
                  checked={responses[q.id] === idx}
                  onChange={() => handleSelect(q.id, idx)}
                />
                <span>{opt}</span>
              </label>
            ))}
          </div>
          {submitted && (
            <p
              className={`mt-2 text-sm ${
                responses[q.id] === q.answer
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {responses[q.id] === q.answer ? "Correct!" : "Incorrect"}
            </p>
          )}
        </div>
      ))}
      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
      >
        Submit
      </button>
    </div>
  );
}
