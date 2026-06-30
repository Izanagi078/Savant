// components/PerformanceChart.tsx
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
  Filler
);

interface Attempt {
  id: number;
  topic: string;
  score: number;
  total: number;
  percentage: number;
  timestamp: string;
}

interface PerformanceChartProps {
  attempts: Attempt[];
}

export default function PerformanceChart({ attempts }: PerformanceChartProps) {
  // Sort attempts chronologically by timestamp
  const sortedAttempts = [...attempts].sort(
    (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  );

  const data = {
    labels: sortedAttempts.map((_, i) => `Attempt ${i + 1}`),
    datasets: [
      {
        label: "Quiz Score",
        data: sortedAttempts.map((a) => a.percentage),
        borderColor: "rgb(6, 182, 212)", // Cyan-500
        backgroundColor: "rgba(6, 182, 212, 0.15)",
        fill: true,
        tension: 0.35,
        pointBackgroundColor: "rgb(6, 182, 212)",
        pointHoverBackgroundColor: "#ffffff",
        pointHoverBorderColor: "rgb(6, 182, 212)",
        pointHoverRadius: 7,
        pointRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: "#090d16",
        titleColor: "#94a3b8",
        bodyColor: "#ffffff",
        borderColor: "rgba(6, 182, 212, 0.3)",
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
        displayColors: false,
        callbacks: {
          title: (context: any) => {
            const index = context[0].dataIndex;
            return `Topic: ${sortedAttempts[index].topic}`;
          },
          label: (context: any) => {
            const index = context.dataIndex;
            const attempt = sortedAttempts[index];
            const dateStr = new Date(attempt.timestamp).toLocaleDateString(undefined, {
              month: "short",
              day: "numeric",
              hour: "2-digit",
              minute: "2-digit",
            });
            return [
              `Score: ${attempt.score}/${attempt.total} (${Math.round(attempt.percentage)}%)`,
              `Date: ${dateStr}`,
            ];
          },
        },
      },
    },
    scales: {
      y: {
        min: 0,
        max: 100,
        grid: {
          color: "rgba(63, 63, 70, 0.15)",
        },
        ticks: {
          color: "#a1a1aa",
          callback: (value: any) => `${value}%`,
          font: {
            size: 10,
          },
        },
      },
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: "#a1a1aa",
          font: {
            size: 10,
          },
        },
      },
    },
  };

  return (
    <div className="relative h-[320px] w-full">
      <Line data={data} options={options} />
    </div>
  );
}
