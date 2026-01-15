import { useState } from 'react'
import {
  LayoutDashboard,
  Wallet,
  PieChart,
  Settings,
  Bell,
  Search,
  ArrowUpRight,
  ArrowDownLeft,
  Plus,
  TrendingUp,
  CreditCard,
  DollarSign
} from 'lucide-react'
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts'
import { motion } from 'framer-motion'
import './App.css'

const data = [
  { name: 'Mon', income: 4000, expenses: 2400 },
  { name: 'Tue', income: 3000, expenses: 1398 },
  { name: 'Wed', income: 2000, expenses: 9800 },
  { name: 'Thu', income: 2780, expenses: 3908 },
  { name: 'Fri', income: 1890, expenses: 4800 },
  { name: 'Sat', income: 2390, expenses: 3800 },
  { name: 'Sun', income: 3490, expenses: 4300 },
]

const StatCard = ({ title, value, change, icon: Icon, trend }: any) => (
  <motion.div
    whileHover={{ scale: 1.02 }}
    className="glass-card p-6 flex flex-col gap-4"
  >
    <div className="flex justify-between items-start">
      <div className="p-3 bg-white/5 rounded-xl">
        <Icon size={24} className="text-secondary" />
      </div>
      <div className={`flex items-center gap-1 text-sm ${trend === 'up' ? 'text-success' : 'text-danger'}`}>
        {trend === 'up' ? <TrendingUp size={16} /> : <TrendingUp size={16} className="rotate-180" />}
        {change}%
      </div>
    </div>
    <div>
      <p className="text-text-muted text-sm font-medium">{title}</p>
      <h3 className="text-2xl font-bold mt-1">${value.toLocaleString()}</h3>
    </div>
  </motion.div>
)

const TransactionItem = ({ name, category, amount, date, type }: any) => (
  <div className="flex items-center justify-between p-4 bg-white/5 rounded-2xl mb-3 hover:bg-white/10 transition-colors cursor-pointer">
    <div className="flex items-center gap-4">
      <div className={`p-3 rounded-xl ${type === 'income' ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'}`}>
        {type === 'income' ? <ArrowDownLeft size={20} /> : <ArrowUpRight size={20} />}
      </div>
      <div>
        <p className="font-semibold text-text">{name}</p>
        <p className="text-xs text-text-muted">{category} • {date}</p>
      </div>
    </div>
    <p className={`font-bold ${type === 'income' ? 'text-success' : 'text-text'}`}>
      {type === 'income' ? '+' : '-'}${Math.abs(amount).toFixed(2)}
    </p>
  </div>
)

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-72 border-r border-glass-border p-6 flex flex-col fixed h-full bg-background/50 backdrop-blur-xl z-20">
        <div className="flex items-center gap-3 px-2 mb-10">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center">
            <Wallet className="text-white" size={24} />
          </div>
          <h1 className="text-2xl font-bold tracking-tight gradient-text">Lumina</h1>
        </div>

        <nav className="flex-1 space-y-2">
          {[
            { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
            { id: 'transactions', icon: CreditCard, label: 'Transactions' },
            { id: 'analytics', icon: PieChart, label: 'Analytics' },
            { id: 'settings', icon: Settings, label: 'Settings' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center gap-4 px-4 py-3 rounded-xl transition-all ${activeTab === item.id
                ? 'bg-primary/20 text-primary border border-primary/30'
                : 'text-text-muted hover:bg-white/5'
                }`}
            >
              <item.icon size={20} />
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="mt-auto">
          <div className="glass-card p-4 bg-primary/10 border-primary/20">
            <p className="text-xs font-semibold text-primary uppercase tracking-wider mb-2">Upgrade Pro</p>
            <p className="text-sm text-text-muted mb-4">Get AI-powered financial insights and more.</p>
            <button className="btn-primary w-full text-sm py-2">Go Premium</button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-72 p-8">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h2 className="text-3xl font-bold">Welcome back, Alex</h2>
            <p className="text-text-muted">Here's what's happening with your money today.</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={18} />
              <input
                type="text"
                placeholder="Search..."
                className="bg-white/5 border border-glass-border rounded-xl py-2 pl-10 pr-4 focus:outline-none focus:border-primary/50 transition-colors w-64"
              />
            </div>
            <button className="p-2 glass-card rounded-xl relative">
              <Bell size={20} className="text-text-muted" />
              <span className="absolute top-2 right-2 w-2 h-2 bg-primary rounded-full"></span>
            </button>
            <div className="w-10 h-10 rounded-xl overflow-hidden border border-glass-border">
              <img src="https://ui-avatars.com/api/?name=Alex+Rivers&background=8b5cf6&color=fff" alt="Avatar" />
            </div>
          </div>
        </header>

        <div className="grid grid-cols-3 gap-6 mb-8">
          <StatCard title="Total Balance" value={48250.00} change={12.5} icon={Wallet} trend="up" />
          <StatCard title="Monthly Income" value={12400.00} change={8.2} icon={DollarSign} trend="up" />
          <StatCard title="Monthly Expense" value={3820.00} change={2.4} icon={ArrowUpRight} trend="down" />
        </div>

        <div className="grid grid-cols-3 gap-8">
          {/* Main Chart */}
          <div className="col-span-2 glass-card p-6">
            <div className="flex justify-between items-center mb-8">
              <h3 className="text-xl font-bold">Revenue Flow</h3>
              <select className="bg-white/5 border border-glass-border rounded-lg px-3 py-1 text-sm focus:outline-none">
                <option>Last 7 Days</option>
                <option>Last 30 Days</option>
              </select>
            </div>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data}>
                  <defs>
                    <linearGradient id="colorIncome" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorExpense" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis
                    dataKey="name"
                    axisLine={false}
                    tickLine={false}
                    tick={{ fill: '#9ca3af', fontSize: 12 }}
                  />
                  <YAxis
                    hide
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#111827',
                      borderColor: 'rgba(255,255,255,0.1)',
                      borderRadius: '12px',
                      color: '#f9fafb'
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="income"
                    stroke="#8b5cf6"
                    strokeWidth={3}
                    fillOpacity={1}
                    fill="url(#colorIncome)"
                  />
                  <Area
                    type="monotone"
                    dataKey="expenses"
                    stroke="#06b6d4"
                    strokeWidth={3}
                    fillOpacity={1}
                    fill="url(#colorExpense)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Recent Transactions */}
          <div className="glass-card p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold">Recent Activity</h3>
              <button className="text-sm text-primary font-medium hover:underline">See All</button>
            </div>
            <div className="space-y-1">
              <TransactionItem name="Apple Store" category="Electronics" amount={-999.00} date="Just now" type="expense" />
              <TransactionItem name="Salary Deposit" category="Work" amount={8500.00} date="2 hours ago" type="income" />
              <TransactionItem name="Netflix" category="Subscription" amount={-15.99} date="Yesterday" type="expense" />
              <TransactionItem name="Starbucks" category="Food" amount={-12.40} date="Yesterday" type="expense" />
            </div>
            <button className="w-full mt-4 flex items-center justify-center gap-2 py-4 border-2 border-dashed border-glass-border rounded-2xl text-text-muted hover:border-primary/50 hover:text-primary transition-all">
              <Plus size={20} />
              <span className="font-medium">Add Transaction</span>
            </button>
          </div>
        </div>
      </main>

      {/* Floating Action Button for mobile or quick access */}
      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="fixed bottom-8 right-8 w-16 h-16 bg-primary rounded-full shadow-lg shadow-primary/20 flex items-center justify-center text-white z-30"
      >
        <Plus size={32} />
      </motion.button>
    </div>
  )
}

export default App
