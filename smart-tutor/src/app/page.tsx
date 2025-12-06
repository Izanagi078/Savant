"use client";

import { useState } from "react";

export default function QuizPage() {
  const [answer, setAnswer] = useState("");

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-blue-700">Welcome to the learning app</h1>
      <p className="mt-4 text-gray-700">
        Test your knowledge with quick interactive questions.
      </p>

      <div className="mt-6 bg-white shadow rounded-lg p-4">
        <h2 className="text-xl font-semibold">Q1: Which language is primarily used for styling web pages?</h2>
        <div className="mt-4 flex flex-col gap-2">
          {["CSS", "Python", "SQL"].map((option) => (
            <button
              key={option}
              onClick={() => setAnswer(option)}
              className={`px-4 py-2 rounded border ${
                answer === option
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 hover:bg-gray-200"
              }`}
            >
              {option}
            </button>
          ))}
        </div>
        {answer && (
          <p className="mt-4 font-medium">
            You selected: <span className="text-blue-600">{answer}</span>
          </p>
        )}
      </div>
    </div>
  );
}
