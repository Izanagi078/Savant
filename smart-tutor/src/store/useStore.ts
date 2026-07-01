import { create } from "zustand";

interface Resource {
  source: string;
  title: string;
  description: string;
  url: string;
}

interface Module {
  title: string;
  description: string;
  key_concepts: string[];
  resources?: Resource[];
}

interface Syllabus {
  title: string;
  description: string;
  modules: Module[];
}

interface ChatMessage {
  role: string;
  text: string;
}

interface CourseState {
  currentRequestId: string;
  topic: string;
  level: string;
  syllabus: Syllabus | null;
  activeModuleIndex: number | null;
  chatHistory: ChatMessage[];
  
  setCurrentRequestId: (id: string) => void;
  setTopic: (topic: string) => void;
  setLevel: (level: string) => void;
  setSyllabus: (syllabus: Syllabus | null) => void;
  setActiveModuleIndex: (index: number | null) => void;
  setChatHistory: (history: ChatMessage[]) => void;
  addChatMessage: (message: ChatMessage) => void;
  resetCourse: () => void;
}

export const useCourseStore = create<CourseState>((set) => ({
  currentRequestId: "",
  topic: "",
  level: "beginner",
  syllabus: null,
  activeModuleIndex: 0,
  chatHistory: [],

  setCurrentRequestId: (id) => set({ currentRequestId: id }),
  setTopic: (topic) => set({ topic }),
  setLevel: (level) => set({ level }),
  setSyllabus: (syllabus) => set({ syllabus }),
  setActiveModuleIndex: (index) => set({ activeModuleIndex: index }),
  setChatHistory: (chatHistory) => set({ chatHistory }),
  addChatMessage: (message) => set((state) => ({ chatHistory: [...state.chatHistory, message] })),
  resetCourse: () => set({
    currentRequestId: "",
    topic: "",
    level: "beginner",
    syllabus: null,
    activeModuleIndex: 0,
    chatHistory: []
  })
}));
