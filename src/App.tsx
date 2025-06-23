import React, { useState } from 'react'
import { Search, MapPin, TrendingUp, Users, BookOpen, Compass, Menu, X } from 'lucide-react'

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const features = [
    {
      icon: <Compass className="w-8 h-8 text-teal-600" />,
      title: "Career Path Discovery",
      description: "Explore diverse career opportunities tailored to Singapore's job market with AI-powered insights."
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-teal-600" />,
      title: "Market Intelligence",
      description: "Get real-time salary benchmarks, industry trends, and growth projections for informed decisions."
    },
    {
      icon: <BookOpen className="w-8 h-8 text-teal-600" />,
      title: "Skills Gap Analysis",
      description: "Identify skill gaps and receive personalized learning recommendations to advance your career."
    },
    {
      icon: <Users className="w-8 h-8 text-teal-600" />,
      title: "Industry Networks",
      description: "Connect with professionals and discover networking opportunities in your field of interest."
    }
  ]

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement RAG search functionality
    console.log('Searching for:', searchQuery)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-teal-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-teal-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-teal-100 rounded-full flex items-center justify-center">
                <img 
                  src="https://cdn.chatandbuild.com/users/684bbe2a00d8c4b56fb7f2bb/logo-atlas-1750691366656-709402992.png" 
                  alt="SG Career Atlas" 
                  className="w-8 h-8 object-contain"
                />
              </div>
              <span className="text-xl font-bold text-gray-900">SG Career Atlas</span>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <a href="#" className="text-gray-700 hover:text-teal-600 transition-colors">Explore Careers</a>
              <a href="#" className="text-gray-700 hover:text-teal-600 transition-colors">Market Insights</a>
              <a href="#" className="text-gray-700 hover:text-teal-600 transition-colors">Skills Assessment</a>
              <a href="#" className="text-gray-700 hover:text-teal-600 transition-colors">Resources</a>
              <button className="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors">
                Get Started
              </button>
            </div>

            {/* Mobile menu button */}
            <button 
              className="md:hidden p-2"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="md:hidden py-4 border-t border-teal-100">
              <div className="flex flex-col space-y-3">
                <a href="#" className="text-gray-700 hover:text-teal-600 transition-colors px-2 py-1">Explore Careers</a>
                <a href="#" className="text-gray-700 hover:text-teal-600 transition-colors px-2 py-1">Market Insights</a>
                <a href="#" className="text-gray-700 hover:text-teal-600 transition-colors px-2 py-1">Skills Assessment</a>
                <a href="#" className="text-gray-700 hover:text-teal-600 transition-colors px-2 py-1">Resources</a>
                <button className="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors mx-2 mt-2">
                  Get Started
                </button>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Navigate Your Career Journey with{' '}
              <span className="text-teal-600">AI Intelligence</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Discover personalized career paths, market insights, and growth opportunities 
              tailored specifically for Singapore's dynamic job landscape.
            </p>

            {/* Search Bar */}
            <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-12">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Ask about careers, salaries, skills, or industry trends..."
                  className="w-full pl-12 pr-4 py-4 text-lg border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent shadow-lg"
                />
                <button
                  type="submit"
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-teal-600 text-white px-6 py-2 rounded-lg hover:bg-teal-700 transition-colors"
                >
                  Search
                </button>
              </div>
            </form>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
              <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-teal-100">
                <div className="text-3xl font-bold text-teal-600 mb-2">500+</div>
                <div className="text-gray-600">Career Paths Mapped</div>
              </div>
              <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-teal-100">
                <div className="text-3xl font-bold text-teal-600 mb-2">50K+</div>
                <div className="text-gray-600">Job Market Data Points</div>
              </div>
              <div className="bg-white/60 backdrop-blur-sm rounded-xl p-6 border border-teal-100">
                <div className="text-3xl font-bold text-teal-600 mb-2">95%</div>
                <div className="text-gray-600">User Satisfaction Rate</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powered by Advanced AI Technology
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our RAG-based system combines real-time market data with personalized insights 
              to guide your career decisions with unprecedented accuracy.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-gradient-to-br from-teal-50 to-slate-50 rounded-xl p-6 hover:shadow-lg transition-shadow">
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-teal-600 to-teal-700">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Chart Your Career Course?
          </h2>
          <p className="text-xl text-teal-100 mb-8">
            Join thousands of professionals who've transformed their careers with AI-powered guidance.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-white text-teal-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-50 transition-colors">
              Start Free Assessment
            </button>
            <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-teal-600 transition-colors">
              View Demo
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-teal-600 rounded-full flex items-center justify-center">
                  <img 
                    src="https://cdn.chatandbuild.com/users/684bbe2a00d8c4b56fb7f2bb/logo-atlas-1750691366656-709402992.png" 
                    alt="SG Career Atlas" 
                    className="w-6 h-6 object-contain"
                  />
                </div>
                <span className="text-lg font-bold">SG Career Atlas</span>
              </div>
              <p className="text-gray-400">
                AI-powered career guidance for Singapore professionals.
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Platform</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Career Explorer</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Skills Assessment</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Market Insights</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Learning Paths</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Resources</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Career Guides</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Industry Reports</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Salary Benchmarks</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Success Stories</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="font-semibold mb-4">Company</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 SG Career Atlas. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
