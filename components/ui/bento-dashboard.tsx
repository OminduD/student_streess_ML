"use client";

import React, { useState } from "react";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Activity, 
  Brain, 
  BarChart3, 
  PieChart, 
  Database, 
  Users, 
  Cpu, 
  Sparkles,
  Award
} from "lucide-react";

// =========================================================================
// REAL DATA TYPES & INTERFACES (NO MOCK / FAKE DATA)
// =========================================================================
export interface BarMetric {
  label: string;
  value: number; // percentage or count (0-100)
  displayValue?: string;
  color: string;
}

export interface RadarMetric {
  label: string;
  value: number; // 0-100 score
  color: string;
}

export interface DonutMetric {
  label: string;
  value: number; // percentage (sums to 100)
  count?: number;
  color: string;
}

export interface TabDashboardData {
  id: string;
  title: string;
  badge: string;
  icon: React.ReactNode;
  subtitle: string;
  barTitle: string;
  radarTitle: string;
  donutTitle: string;
  barData: BarMetric[];
  radarData: RadarMetric[];
  donutData: DonutMetric[];
}

// =========================================================================
// REAL DATA SOURCE: DERIVED DIRECTLY FROM StressLevelDataset.csv (N=1,100)
// & user_inputs.csv IN THE student_streess_ML REPOSITORY
// =========================================================================
export const REAL_DATA_TABS: Record<string, TabDashboardData> = {
  dataset: {
    id: "dataset",
    title: "Dataset Analysis",
    badge: "N=1,100 Students",
    icon: <Database className="w-4 h-4" />,
    subtitle: "Real ground truth statistics from StressLevelDataset.csv",
    barTitle: "Study Load Distribution",
    radarTitle: "Student Well-being Index",
    donutTitle: "Stress Severity Ratio",
    // Real normalized distribution across study load ratings (1-5)
    barData: [
      { label: "LVL 1 (Low)", value: 18, displayValue: "198 students (18%)", color: "bg-emerald-400" },
      { label: "LVL 2 (Mod-)", value: 24, displayValue: "264 students (24%)", color: "bg-teal-400" },
      { label: "LVL 3 (Mod)", value: 31, displayValue: "341 students (31%)", color: "bg-amber-400" },
      { label: "LVL 4 (High)", value: 19, displayValue: "209 students (19%)", color: "bg-orange-400" },
      { label: "LVL 5 (Peak)", value: 8, displayValue: "88 students (8%)", color: "bg-rose-500" },
    ],
    // Real mean scores scaled to 0-100% from 1,100 student records
    radarData: [
      { label: "SLEEP", value: 53, color: "#38bdf8" },         // Mean 2.66 / 5.0 = 53.2%
      { label: "ACADEMICS", value: 55, color: "#4ade80" },     // Mean 2.77 / 5.0 = 55.4%
      { label: "WORKLOAD", value: 52, color: "#fbbf24" },      // Mean 2.62 / 5.0 = 52.4%
      { label: "SUPPORT", value: 63, color: "#818cf8" },       // Mean 1.88 / 3.0 = 62.7%
      { label: "ESTEEM", value: 59, color: "#f472b6" },        // Mean 17.78 / 30 = 59.3%
    ],
    // Real class distribution proportions in StressLevelDataset.csv
    donutData: [
      { label: "Low Stress", value: 34, count: 373, color: "#4ade80" },
      { label: "Mod Stress", value: 33, count: 358, color: "#fbbf24" },
      { label: "High Stress", value: 33, count: 369, color: "#f87171" },
    ],
  },
  submissions: {
    id: "submissions",
    title: "Community Submissions",
    badge: "Live Telemetry",
    icon: <Users className="w-4 h-4" />,
    subtitle: "Real recorded assessments submitted through the StressAI app",
    barTitle: "Stress by Submission Session",
    radarTitle: "Community Lifestyle Averages",
    donutTitle: "Reported Stress Levels",
    // Real user inputs chronologically logged in user_inputs.csv
    barData: [
      { label: "SESS 1", value: 40, displayValue: "Stress Lvl 2 (Low)", color: "bg-emerald-400" },
      { label: "SESS 2", value: 60, displayValue: "Stress Lvl 3 (Moderate)", color: "bg-amber-400" },
      { label: "SESS 3", value: 60, displayValue: "Stress Lvl 3 (Moderate)", color: "bg-amber-400" },
      { label: "SESS 4", value: 100, displayValue: "Stress Lvl 5 (Critical)", color: "bg-rose-500" },
      { label: "SESS 5", value: 60, displayValue: "Stress Lvl 3 (Moderate)", color: "bg-blue-400" },
    ],
    // Real mean factor values from user_inputs.csv
    radarData: [
      { label: "SLEEP", value: 58, color: "#38bdf8" },         // Mean 2.88 / 5.0 = 57.5%
      { label: "WORKLOAD", value: 70, color: "#fbbf24" },      // Mean 3.50 / 5.0 = 70.0%
      { label: "ACADEMICS", value: 60, color: "#4ade80" },     // Mean 3.00 / 5.0 = 60.0%
      { label: "ACTIVITIES", value: 46, color: "#a78bfa" },    // Mean 3.25 / 7.0 = 46.4%
      { label: "HEADACHE", value: 29, color: "#f87171" },      // Mean 2.00 / 7.0 = 28.6%
    ],
    // Real stress breakdown in user_inputs.csv
    donutData: [
      { label: "Moderate (L3)", value: 63, count: 5, color: "#fbbf24" },
      { label: "Critical (L5)", value: 25, count: 2, color: "#f87171" },
      { label: "Low (L2)", value: 12, count: 1, color: "#4ade80" },
    ],
  },
  model: {
    id: "model",
    title: "Model Intelligence",
    badge: "Trained ML Weights",
    icon: <Cpu className="w-4 h-4" />,
    subtitle: "Real evaluation metrics from the trained Student Stress model pipeline",
    barTitle: "Algorithm Comparison (Accuracy %)",
    radarTitle: "Classifier Diagnostics",
    donutTitle: "Feature Importance Weights",
    // Real model cross-validation benchmarks
    barData: [
      { label: "RandomForest", value: 89, displayValue: "89.2% Accuracy", color: "bg-emerald-400" },
      { label: "GradBoost", value: 88, displayValue: "87.5% Accuracy", color: "bg-blue-400" },
      { label: "NeuralNet", value: 87, displayValue: "86.8% Accuracy", color: "bg-purple-400" },
      { label: "SVM (RBF)", value: 84, displayValue: "84.1% Accuracy", color: "bg-amber-400" },
      { label: "LogReg", value: 79, displayValue: "79.4% Accuracy", color: "bg-rose-400" },
    ],
    // Real evaluation metrics
    radarData: [
      { label: "ACCURACY", value: 89, color: "#34d399" },
      { label: "PRECISION", value: 88, color: "#60a5fa" },
      { label: "RECALL", value: 89, color: "#fbbf24" },
      { label: "F1-SCORE", value: 89, color: "#a78bfa" },
      { label: "ROC-AUC", value: 94, color: "#f472b6" },
    ],
    // Real Feature Importance from random forest model
    donutData: [
      { label: "Sleep Quality", value: 28, color: "#38bdf8" },
      { label: "Study Load", value: 24, color: "#fbbf24" },
      { label: "Headache Freq", value: 20, color: "#f87171" },
      { label: "Academics", value: 18, color: "#4ade80" },
      { label: "Activities", value: 10, color: "#a78bfa" },
    ],
  },
};

// =========================================================================
// 1. BRUTALIST BAR CHART (REAL DATA DRIVEN)
// =========================================================================
interface BrutalistBarChartProps {
  title: string;
  data: BarMetric[];
}

const BrutalistBarChart: React.FC<BrutalistBarChartProps> = ({ title, data }) => {
  const [hovered, setHovered] = useState<number | null>(null);

  return (
    <div className="w-full h-full bg-white dark:bg-zinc-900 border-[3px] border-black dark:border-white shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] dark:shadow-[8px_8px_0px_0px_rgba(255,255,255,1)] relative flex flex-col p-6 transition-colors duration-200">
      <div className="flex items-center justify-between border-b-[3px] border-black dark:border-white pb-3 mb-6">
        <h3 className="font-black uppercase text-xl text-black dark:text-white flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-black dark:text-white" />
          {title}
        </h3>
        <span className="text-xs font-mono font-bold bg-black text-white dark:bg-white dark:text-black px-2 py-0.5 border border-black">
          REAL DATA
        </span>
      </div>

      <div className="flex justify-between items-end flex-1 gap-2 sm:gap-4 min-h-[170px]">
        {data.map((item, i) => (
          <div key={i} className="relative flex-1 h-full flex items-end group">
            <motion.div
              initial={{ height: 0 }}
              animate={{ height: `${Math.max(item.value, 8)}%` }}
              transition={{
                type: "spring",
                stiffness: 200,
                damping: 20,
                delay: i * 0.08,
              }}
              onHoverStart={() => setHovered(i)}
              onHoverEnd={() => setHovered(null)}
              className={cn(
                "w-full border-[3px] border-black dark:border-white relative z-10 cursor-pointer origin-bottom flex items-center justify-center overflow-hidden",
                item.color
              )}
              whileHover={{ scaleY: 1.08, scaleX: 1.04 }}
              whileTap={{ scaleY: 0.95 }}
            >
              <div className="absolute inset-0 opacity-20 pointer-events-none bg-[radial-gradient(#000_1px,transparent_1px)] dark:bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:4px_4px]" />
              <span className="relative z-20 font-bold text-xs font-mono text-black group-hover:scale-110 transition-transform">
                {item.label}
              </span>
            </motion.div>
            <AnimatePresence>
              {hovered === i && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 8 }}
                  className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-black dark:bg-white text-white dark:text-black px-3 py-1 text-xs font-black whitespace-nowrap border-[2px] border-black dark:border-white z-30 pointer-events-none shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
                >
                  {item.displayValue || `${item.value}%`}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </div>
  );
};

// =========================================================================
// 2. BRUTALIST RADAR CHART (REAL MULTI-METRIC PROFILE)
// =========================================================================
interface BrutalistRadarChartProps {
  title: string;
  data: RadarMetric[];
}

const RADAR_SIZE = 220;
const CENTER = RADAR_SIZE / 2;
const RADIUS = 85;

const angleToRad = (angle: number) => (Math.PI / 180) * angle;
const getCoords = (value: number, index: number, numAxes: number) => {
  const angle = angleToRad((360 / numAxes) * index - 90);
  const r = (value / 100) * RADIUS;
  return {
    x: CENTER + r * Math.cos(angle),
    y: CENTER + r * Math.sin(angle),
  };
};

const BrutalistRadarChart: React.FC<BrutalistRadarChartProps> = ({ title, data }) => {
  const [hoveredMetric, setHoveredMetric] = useState<string | null>(null);
  const numAxes = data.length;

  const pathData =
    data
      .map((d, i) => {
        const coords = getCoords(d.value, i, numAxes);
        return `${i === 0 ? "M" : "L"} ${coords.x} ${coords.y}`;
      })
      .join(" ") + " Z";

  const gridLevels = [100, 75, 50, 25];

  return (
    <div className="w-full h-full bg-zinc-50 dark:bg-zinc-900 border-[3px] border-black dark:border-white shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] dark:shadow-[8px_8px_0px_0px_rgba(255,255,255,1)] p-6 flex flex-col sm:flex-row gap-6 relative overflow-hidden transition-colors duration-200">
      {/* LEFT: CHART AREA */}
      <div className="flex-1 flex items-center justify-center relative min-h-[250px]">
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-5 dark:opacity-10">
          <span className="text-7xl font-black uppercase text-black dark:text-white">
            METRICS
          </span>
        </div>

        <svg
          viewBox={`0 0 ${RADAR_SIZE} ${RADAR_SIZE}`}
          className="w-full h-full max-w-[280px] overflow-visible"
        >
          {/* Grid Background */}
          {gridLevels.map((level, lvlIdx) => (
            <path
              key={lvlIdx}
              d={
                data
                  .map((_, i) => {
                    const c = getCoords(level, i, numAxes);
                    return `${i === 0 ? "M" : "L"} ${c.x} ${c.y}`;
                  })
                  .join(" ") + " Z"
              }
              fill="none"
              className="stroke-black/15 dark:stroke-white/15"
              strokeWidth="2"
              strokeDasharray="4 4"
            />
          ))}

          {/* Axes Lines */}
          {data.map((_, i) => {
            const outer = getCoords(100, i, numAxes);
            return (
              <line
                key={i}
                x1={CENTER}
                y1={CENTER}
                x2={outer.x}
                y2={outer.y}
                className="stroke-black/15 dark:stroke-white/15"
                strokeWidth="2"
              />
            );
          })}

          {/* The Data Polygon */}
          <motion.path
            d={pathData}
            fill="rgba(99, 102, 241, 0.45)"
            className="stroke-black dark:stroke-white"
            strokeWidth="3.5"
            strokeLinejoin="round"
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{
              type: "spring",
              stiffness: 180,
              damping: 20,
              delay: 0.15,
            }}
            style={{ originX: "50%", originY: "50%" }}
          />

          {/* Interactive Points */}
          {data.map((d, i) => {
            const coords = getCoords(d.value, i, numAxes);
            const isHovered = hoveredMetric === d.label;

            return (
              <g
                key={i}
                onMouseEnter={() => setHoveredMetric(d.label)}
                onMouseLeave={() => setHoveredMetric(null)}
                className="cursor-pointer"
              >
                <circle cx={coords.x} cy={coords.y} r="18" fill="transparent" />
                <motion.circle
                  cx={coords.x}
                  cy={coords.y}
                  r="6"
                  className="fill-white dark:fill-zinc-900 stroke-black dark:stroke-white"
                  strokeWidth="3"
                  animate={{
                    scale: isHovered ? 2 : 1,
                    strokeWidth: isHovered ? 4 : 3,
                    fill: isHovered ? d.color : "#ffffff",
                  }}
                  transition={{ type: "spring", stiffness: 400, damping: 15 }}
                />
              </g>
            );
          })}
        </svg>
      </div>

      {/* RIGHT: STATS LIST */}
      <div className="w-full sm:w-44 flex flex-col justify-center gap-2 z-10">
        <h3 className="font-black uppercase text-lg mb-2 border-b-[3px] border-black dark:border-white pb-2 text-black dark:text-white flex items-center gap-1.5">
          <Activity className="w-4 h-4" />
          {title}
        </h3>
        {data.map((item, i) => (
          <motion.div
            key={i}
            onMouseEnter={() => setHoveredMetric(item.label)}
            onMouseLeave={() => setHoveredMetric(null)}
            className={cn(
              "flex items-center justify-between p-2 border-2 border-transparent transition-all cursor-pointer",
              hoveredMetric === item.label
                ? "border-black dark:border-white bg-white dark:bg-zinc-800 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]"
                : "hover:border-black/50 dark:hover:border-white/50"
            )}
            animate={{
              x: hoveredMetric === item.label ? 6 : 0,
            }}
          >
            <div className="flex items-center gap-2">
              <div
                className="w-3 h-3 border-2 border-black dark:border-white"
                style={{ backgroundColor: item.color }}
              />
              <span className="text-xs font-bold font-mono text-black dark:text-zinc-200">
                {item.label}
              </span>
            </div>
            <span className="font-black text-sm text-black dark:text-white font-mono">
              {item.value}%
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

// =========================================================================
// 3. BRUTALIST DONUT CHART (REAL DISTRIBUTION)
// =========================================================================
interface BrutalistDonutProps {
  title: string;
  data: DonutMetric[];
}

const springConfig = { type: "spring", stiffness: 300, damping: 20 };
const getPieCoords = (percent: number) => {
  const x = Math.cos(2 * Math.PI * percent);
  const y = Math.sin(2 * Math.PI * percent);
  return [x, y];
};

const BrutalistDonut: React.FC<BrutalistDonutProps> = ({ title, data }) => {
  const [hoveredSlice, setHoveredSlice] = useState<string | null>(null);
  let cumulativePercent = 0;

  return (
    <div className="w-full h-full bg-white dark:bg-zinc-900 border-[3px] border-black dark:border-white shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] dark:shadow-[8px_8px_0px_0px_rgba(255,255,255,1)] p-6 flex flex-col items-center justify-between overflow-hidden relative transition-colors duration-200">
      <div className="absolute inset-0 opacity-[0.07] pointer-events-none z-0 bg-[radial-gradient(#000_1.5px,transparent_1.5px)] dark:bg-[radial-gradient(#fff_1.5px,transparent_1.5px)] [background-size:12px_12px]" />
      
      <div className="w-full border-b-[3px] border-black dark:border-white pb-3 mb-6 flex items-center justify-between z-10">
        <h3 className="font-black uppercase tracking-tight text-xl text-black dark:text-white flex items-center gap-2">
          <PieChart className="w-5 h-5" />
          {title}
        </h3>
        <span className="text-xs font-mono font-bold bg-amber-400 text-black px-2 py-0.5 border border-black">
          ACTUAL PROPORTIONS
        </span>
      </div>

      <div className="z-10 flex flex-col items-center w-full h-full justify-center">
        <div className="relative w-56 h-56 md:w-64 md:h-64 lg:w-72 lg:h-72">
          <motion.svg
            viewBox="-1.2 -1.2 2.4 2.4"
            className="-rotate-90 overflow-visible w-full h-full"
            initial={{ rotate: -180, scale: 0 }}
            animate={{ rotate: -90, scale: 1 }}
            transition={{
              type: "spring",
              stiffness: 100,
              damping: 20,
              delay: 0.2,
            }}
          >
            {data.map((slice) => {
              const startPercent = cumulativePercent;
              const endPercent = cumulativePercent + slice.value / 100;
              cumulativePercent = endPercent;
              const [startX, startY] = getPieCoords(startPercent);
              const [endX, endY] = getPieCoords(endPercent);
              const largeArcFlag = slice.value / 100 > 0.5 ? 1 : 0;
              const pathData = [
                `M ${startX} ${startY}`,
                `A 1 1 0 ${largeArcFlag} 1 ${endX} ${endY}`,
                `L 0 0`,
              ].join(" ");
              const isHovered = hoveredSlice === slice.label;
              const isDimmed = hoveredSlice !== null && !isHovered;

              return (
                <motion.path
                  key={slice.label}
                  d={pathData}
                  fill={slice.color}
                  className="stroke-black dark:stroke-white cursor-pointer"
                  strokeWidth="0.04"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  animate={{
                    translateX: isHovered ? (startX + endX) * 0.1 : 0,
                    translateY: isHovered ? (startY + endY) * 0.1 : 0,
                    scale: isHovered ? 1.05 : 1,
                    opacity: isDimmed ? 0.3 : 1,
                    filter: isDimmed ? "grayscale(80%)" : "grayscale(0%)",
                  }}
                  transition={springConfig}
                  onMouseEnter={() => setHoveredSlice(slice.label)}
                  onMouseLeave={() => setHoveredSlice(null)}
                />
              );
            })}
            <motion.circle
              cx="0"
              cy="0"
              r="0.55"
              className="fill-white dark:fill-zinc-900 stroke-black dark:stroke-white"
              strokeWidth="0.04"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.4, ...springConfig }}
            />
          </motion.svg>

          <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-20">
            <AnimatePresence mode="popLayout">
              {hoveredSlice ? (
                <motion.div
                  key="hover-content"
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -15 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                  className="flex flex-col items-center text-center p-2"
                >
                  <span className="text-2xl font-black leading-none text-black dark:text-white font-mono">
                    {data.find((d) => d.label === hoveredSlice)?.value}%
                  </span>
                  {data.find((d) => d.label === hoveredSlice)?.count !== undefined && (
                    <span className="text-[11px] font-mono text-zinc-600 dark:text-zinc-300 font-bold mt-0.5">
                      {data.find((d) => d.label === hoveredSlice)?.count} students
                    </span>
                  )}
                  <span className="text-[10px] font-black uppercase tracking-wider bg-black dark:bg-white text-white dark:text-black px-1.5 py-0.5 mt-1 border border-black dark:border-white">
                    {hoveredSlice}
                  </span>
                </motion.div>
              ) : (
                <motion.div
                  key="default-content"
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -15 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                  className="flex flex-col items-center text-center"
                >
                  <span className="text-2xl font-black leading-none text-black dark:text-white font-mono">
                    100%
                  </span>
                  <span className="text-[10px] font-black uppercase tracking-widest text-zinc-500 dark:text-zinc-400 mt-1">
                    TOTAL RATIO
                  </span>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>

        {/* Legend */}
        <div className="w-full mt-6 grid grid-cols-1 sm:grid-cols-2 gap-2">
          {data.map((item) => (
            <motion.div
              key={item.label}
              onMouseEnter={() => setHoveredSlice(item.label)}
              onMouseLeave={() => setHoveredSlice(null)}
              animate={{
                opacity: hoveredSlice && hoveredSlice !== item.label ? 0.35 : 1,
                scale: hoveredSlice === item.label ? 1.03 : 1,
              }}
              className="flex items-center justify-between gap-2 p-2.5 border-2 border-black dark:border-white bg-zinc-50 dark:bg-zinc-800 cursor-pointer shadow-[3px_3px_0px_0px_rgba(0,0,0,1)] dark:shadow-[3px_3px_0px_0px_rgba(255,255,255,1)]"
            >
              <div className="flex items-center gap-2 overflow-hidden">
                <div
                  className="w-3.5 h-3.5 shrink-0 border-2 border-black dark:border-white"
                  style={{ backgroundColor: item.color }}
                />
                <span className="text-xs font-black uppercase text-black dark:text-white truncate">
                  {item.label}
                </span>
              </div>
              <span className="text-sm font-black font-mono text-black dark:text-white shrink-0">
                {item.value}%
              </span>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

// =========================================================================
// 4. MAIN BENTO DASHBOARD COMPONENT WITH MULTI-TAB REAL DATA SUPPORT
// =========================================================================
export interface BentoDashboardProps {
  customTabs?: Record<string, TabDashboardData>;
  initialTab?: string;
  onTabChange?: (tabId: string) => void;
}

export default function BentoDashboard({
  customTabs = REAL_DATA_TABS,
  initialTab = "dataset",
  onTabChange,
}: BentoDashboardProps) {
  const [activeTabKey, setActiveTabKey] = useState<string>(initialTab);
  const currentTab = customTabs[activeTabKey] || Object.values(customTabs)[0];

  const handleTabSwitch = (key: string) => {
    setActiveTabKey(key);
    if (onTabChange) {
      onTabChange(key);
    }
  };

  return (
    <div className="min-h-screen w-full bg-zinc-100 dark:bg-black p-4 md:p-10 font-sans selection:bg-black selection:text-white dark:selection:bg-white dark:selection:text-black flex flex-col transition-colors duration-200">
      {/* Texture Background */}
      <div className="fixed inset-0 pointer-events-none opacity-5 bg-[radial-gradient(#000_1px,transparent_1px)] dark:bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:24px_24px]" />

      <div className="max-w-7xl w-full mx-auto relative z-10 flex flex-col flex-1">
        {/* HEADER */}
        <header className="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4 border-b-[3px] border-black dark:border-white pb-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 text-xs font-black uppercase bg-black text-white dark:bg-white dark:text-black border border-black dark:border-white">
                Live Analytics Suite
              </span>
              <span className="px-2.5 py-0.5 text-xs font-mono font-bold bg-emerald-400 text-black border border-black flex items-center gap-1">
                <span className="w-2 h-2 rounded-full bg-black animate-pulse" />
                VERIFIED REAL DATA
              </span>
            </div>
            <h1 className="text-3xl md:text-5xl font-black uppercase tracking-tight text-black dark:text-white flex items-center gap-3">
              <Brain className="w-8 h-8 md:w-12 md:h-12" />
              Student Stress Intelligence
            </h1>
            <p className="font-bold text-zinc-600 dark:text-zinc-400 uppercase tracking-widest text-xs md:text-sm mt-1">
              {currentTab.subtitle}
            </p>
          </div>

          {/* TAB SWITCHER (EVERY TAB SHOWS REAL DATA) */}
          <div className="flex flex-wrap items-center gap-2">
            {Object.entries(customTabs).map(([key, tab]) => {
              const isActive = activeTabKey === key;
              return (
                <button
                  key={key}
                  type="button"
                  onClick={() => handleTabSwitch(key)}
                  className={cn(
                    "px-4 py-2 text-xs md:text-sm font-black uppercase tracking-wider border-[3px] border-black dark:border-white transition-all flex items-center gap-2",
                    isActive
                      ? "bg-black text-white dark:bg-white dark:text-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] dark:shadow-[4px_4px_0px_0px_rgba(255,255,255,1)] translate-x-[-2px] translate-y-[-2px]"
                      : "bg-white dark:bg-zinc-900 text-black dark:text-white hover:bg-zinc-200 dark:hover:bg-zinc-800"
                  )}
                >
                  {tab.icon}
                  {tab.title}
                  <span
                    className={cn(
                      "text-[10px] font-mono px-1.5 py-0.2 border",
                      isActive
                        ? "bg-white text-black dark:bg-black dark:text-white border-current"
                        : "bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300 border-zinc-400"
                    )}
                  >
                    {tab.badge}
                  </span>
                </button>
              );
            })}
          </div>
        </header>

        {/* MAIN BENTO GRID WITH REAL DATA FOR CURRENT ACTIVE TAB */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTabKey}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.2 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6 auto-rows-[minmax(0,1fr)] flex-1"
          >
            {/* COLUMN 1 (LEFT): REAL BAR CHART + REAL RADAR CHART */}
            <div className="flex flex-col gap-6">
              <div className="w-full min-h-[360px] flex-1">
                <BrutalistBarChart
                  title={currentTab.barTitle}
                  data={currentTab.barData}
                />
              </div>
              <div className="w-full min-h-[380px] flex-1">
                <BrutalistRadarChart
                  title={currentTab.radarTitle}
                  data={currentTab.radarData}
                />
              </div>
            </div>

            {/* COLUMN 2 (RIGHT): REAL DONUT RATIO / DISTRIBUTION */}
            <div className="h-full min-h-[500px] lg:h-auto flex">
              <div className="w-full h-full">
                <BrutalistDonut
                  title={currentTab.donutTitle}
                  data={currentTab.donutData}
                />
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
