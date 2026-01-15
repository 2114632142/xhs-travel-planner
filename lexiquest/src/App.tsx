import { useState } from 'react'
import {
  BookOpen,
  Trophy,
  Layers,
  Settings,
  Search,
  Flame,
  ArrowRight,
  Volume2,
  CheckCircle2,
  Calendar,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

// --- Mock Data ---
const VOCAB_DATA = [
  { word: 'Ephemeral', phonetics: '/ɪˈfem.ər.əl/', meaning: 'Lasting for a very short time.', example: 'The autumnal colors are beautiful but ephemeral.' },
  { word: 'Serendipity', phonetics: '/ˌser.ənˈdɪp.ə.ti/', meaning: 'The occurrence of events by chance in a happy way.', example: 'Nature has created wonderful serendipity for us.' },
  { word: 'Eloquent', phonetics: '/ˈel.ə.kwənt/', meaning: 'Fluent or persuasive in speaking or writing.', example: 'He made an eloquent plea for peace.' },
]

// --- Components ---

const SidebarItem = ({ icon: Icon, label, active, onClick }: any) => (
  <button
    onClick={onClick}
    className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all mb-1 ${active ? 'bg-primary text-white shadow-lg shadow-indigo-200' : 'text-text-muted hover:bg-primary-soft hover:text-primary'
      }`}
  >
    <Icon size={20} />
    <span className="font-semibold text-sm tracking-wide">{label}</span>
  </button>
)

const Flashcard = ({ data }: { data: typeof VOCAB_DATA[0] }) => {
  const [isFlipped, setIsFlipped] = useState(false)

  return (
    <div className={`flip-card ${isFlipped ? 'flipped' : ''}`} onClick={() => setIsFlipped(!isFlipped)}>
      <div className="flip-card-inner">
        <div className="flip-card-front p-12">
          <span className="text-primary font-bold tracking-widest text-xs uppercase mb-4">Vocabulary of the Day</span>
          <h2 className="text-6xl mb-6">{data.word}</h2>
          <div className="flex items-center gap-2 text-text-muted mb-8">
            <Volume2 size={20} className="text-primary cursor-pointer hover:scale-110 transition-transform" />
            <span className="font-medium italic">{data.phonetics}</span>
          </div>
          <p className="text-text-muted text-sm">Click to flip and see meaning</p>
        </div>
        <div className="flip-card-back p-12">
          <h3 className="text-2xl font-bold mb-4">Meaning</h3>
          <p className="text-xl leading-relaxed mb-8 opacity-90">{data.meaning}</p>
          <div className="w-16 h-1 bg-white/30 mb-8 rounded-full"></div>
          <h3 className="text-lg font-bold mb-2">Example</h3>
          <p className="italic opacity-80">"{data.example}"</p>
        </div>
      </div>
    </div>
  )
}

function App() {
  const [activeTab, setActiveTab] = useState('learn')
  const [currentCardIdx, setCurrentCardIdx] = useState(0)

  return (
    <div className="flex min-h-screen bg-[#F8FAF8]"> {/* Slight off-white/green for reduced eye strain */}

      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-100 p-6 flex flex-col fixed h-full z-10">
        <div className="flex items-center gap-3 mb-10 px-2">
          <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-100">
            <BookOpen size={24} />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-800">LexiQuest</h1>
        </div>

        <nav className="flex-1">
          <SidebarItem icon={Layers} label="Daily Quest" active={activeTab === 'learn'} onClick={() => setActiveTab('learn')} />
          <SidebarItem icon={CheckCircle2} label="Mastered" active={activeTab === 'mastered'} onClick={() => setActiveTab('mastered')} />
          <SidebarItem icon={Calendar} label="Schedule" active={activeTab === 'schedule'} onClick={() => setActiveTab('schedule')} />
          <SidebarItem icon={Settings} label="Settings" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </nav>

        <div className="mt-auto bg-slate-50 rounded-2xl p-4 border border-slate-100">
          <div className="flex items-center gap-2 mb-3">
            <Flame className="text-orange-500" size={18} />
            <span className="font-bold text-sm">7 Day Streak!</span>
          </div>
          <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div className="bg-orange-500 h-full w-[70%]"></div>
          </div>
          <p className="text-[10px] text-text-muted mt-2 font-medium">3 days until next milestone</p>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-64 p-12 max-w-6xl">

        {/* Header */}
        <header className="flex justify-between items-center mb-12">
          <div>
            <h2 className="text-3xl font-bold text-slate-800 mb-1">Good morning, Explorer</h2>
            <p className="text-text-muted font-medium">Ready to discover 5 new words today?</p>
          </div>
          <div className="flex items-center gap-6">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
              <input
                type="text"
                placeholder="Find a word..."
                className="bg-white border border-slate-200 rounded-xl py-2 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all w-64 shadow-sm"
              />
            </div>
            <div className="flex items-center gap-2 bg-white px-3 py-2 rounded-xl border border-slate-200 shadow-sm">
              <Trophy className="text-yellow-500" size={18} />
              <span className="font-bold text-sm">2,450 XP</span>
            </div>
          </div>
        </header>

        {activeTab === 'learn' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-8"
          >
            {/* Progress Section */}
            <div className="flex items-center justify-between">
              <div className="flex gap-4">
                {[1, 2, 3, 4, 5].map(i => (
                  <div key={i} className={`w-12 h-1.5 rounded-full ${i <= currentCardIdx + 1 ? 'bg-primary' : 'bg-slate-200'}`}></div>
                ))}
              </div>
              <span className="text-sm font-bold text-text-muted">WORD {currentCardIdx + 1} OF 5</span>
            </div>

            {/* Flashcard Area */}
            <div className="flex items-center gap-8">
              <button
                onClick={() => setCurrentCardIdx(Math.max(0, currentCardIdx - 1))}
                className="p-4 rounded-full bg-white border border-slate-200 text-text-muted hover:text-primary transition-colors disabled:opacity-30 shadow-sm"
                disabled={currentCardIdx === 0}
              >
                <ChevronLeft size={24} />
              </button>

              <div className="flex-1 max-w-2xl mx-auto">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={currentCardIdx}
                    initial={{ scale: 0.9, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 1.1, opacity: 0 }}
                    transition={{ type: "spring", stiffness: 200, damping: 20 }}
                  >
                    <Flashcard data={VOCAB_DATA[currentCardIdx % VOCAB_DATA.length]} />
                  </motion.div>
                </AnimatePresence>
              </div>

              <button
                onClick={() => setCurrentCardIdx(Math.min(4, currentCardIdx + 1))}
                className="p-4 rounded-full bg-white border border-slate-200 text-text-muted hover:text-primary transition-colors disabled:opacity-30 shadow-sm"
                disabled={currentCardIdx === 4}
              >
                <ChevronRight size={24} />
              </button>
            </div>

            {/* Actions */}
            <div className="flex justify-center gap-4 pt-4">
              <button className="btn bg-white border border-slate-200 text-text-muted px-8 py-4 hover:bg-slate-50">
                Skip for now
              </button>
              <button className="btn btn-primary px-12 py-4 text-lg">
                I Mastered This <ArrowRight size={20} />
              </button>
            </div>
          </motion.div>
        )}

      </main>

      {/* Floating help/menu */}
      <button className="fixed bottom-10 right-10 w-14 h-14 bg-white border border-slate-200 rounded-full shadow-xl flex items-center justify-center text-primary hover:scale-110 transition-transform">
        <Volume2 size={24} />
      </button>

    </div>
  )
}

export default App
