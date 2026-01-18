import React from 'react';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-white text-gray-900 font-sans">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center ">
              <span className="text-2xl font-bold bg-linear-to-r from-primary to-accent text-green-800 bg-clip-text">
                feedbackflow
              </span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#home" className="text-gray-500 hover:text-gray-900 font-medium transition-colors">Home</a>
              <a href="#features" className="text-gray-500 hover:text-gray-900 font-medium transition-colors">Features</a>
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-gray-500 hover:text-gray-900 font-medium transition-colors">GitHub</a>
            </nav>
            <div>
              <button className="bg-dark text-white px-5 py-2 rounded-full font-medium bg-green-800 hover:bg-green-700 transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">
                Get Started
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="relative overflow-hidden pt-20 pb-24 sm:pt-32 sm:pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <div className="mx-auto max-w-3xl">
            <div className="inline-flex items-center px-4 py-2 text-green-800 rounded-full bg-primary/10 text-primary font-medium text-sm mb-6">
              <span className="animate-pulse mr-2 h-2 w-2 rounded-full bg-primary"></span>
              New: One-click GitHub Integration
            </div>
            <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-gray-900 mb-6 leading-tight">
              Turn User Feedback into <br />
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-green-800">Pull Requests Instantly.</span>
            </h1>
            <p className="mt-4 text-xl text-gray-500 max-w-2xl mx-auto mb-10">
              Connect your repo, embed our widget, and let our AI agent handle the rest. from user report to code fix in minutes.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <button className="px-8 py-4 outline-green-800 bg-primary text-white bg-green-800 text-lg font-bold rounded-xl shadow-lg hover:bg-green-700 hover:outline-green-700 transition-all transform hover:-translate-y-1 hover:shadow-2xl flex items-center justify-center">
                <svg className="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                Connect GitHub
              </button>
              
            </div>
          </div>
          
          {/* Abstract Visual Representation */}
          <div className="mt-20 relative max-w-5xl mx-auto">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-gradient-to-b from-primary/5 to-transparent blur-3xl -z-10"></div>
            <div className="bg-white rounded-2xl shadow-2xl border border-gray-100 p-2 sm:p-4 overflow-hidden">
               <div className="flex flex-col md:flex-row items-center justify-between gap-8 p-8 bg-gray-50/50 rounded-xl">
                 
                 {/* Step 1: Website */}
                 <div className="flex-1 bg-white p-6 rounded-xl shadow-sm border border-gray-200 w-full">
                   <div className="h-3 w-3 bg-red-400 rounded-full mb-4 inline-block mr-1"></div>
                   <div className="h-3 w-3 bg-yellow-400 rounded-full mb-4 inline-block mr-1"></div>
                   <div className="h-3 w-3 bg-green-400 rounded-full mb-4 inline-block"></div>
                   <div className="space-y-3">
                     <div className="h-4 bg-gray-100 rounded w-3/4"></div>
                     <div className="h-20 bg-gray-100 rounded w-full flex items-center justify-center text-gray-400 text-sm border-2 border-dashed border-gray-300">
                       User submits feedback
                     </div>
                   </div>
                 </div>

                 {/* Arrow */}
                 <div className="text-gray-300">
                   <svg className="w-8 h-8 md:w-12 md:h-12 transform rotate-90 md:rotate-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                 </div>

                 {/* Step 2: Agent */}
                 <div className="flex-1 bg-dark text-white p-6 rounded-xl shadow-lg relative overflow-hidden w-full">
                    <div className="absolute top-0 right-0 p-2 opacity-20">
                      <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
                    </div>
                   <h3 className="text-lg font-bold mb-2 flex items-center"><span className="text-secondary mr-2">●</span> AI Agent</h3>
                   <div className="text-gray-400 text-sm space-y-2 font-mono">
                     <p>Running analysis...</p>
                     <p className="text-secondary">Found matching component.</p>
                     <p>Generating fix...</p>
                   </div>
                 </div>

                 {/* Arrow */}
                 <div className="text-gray-300">
                   <svg className="w-8 h-8 md:w-12 md:h-12 transform rotate-90 md:rotate-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                 </div>

                 {/* Step 3: PR */}
                 <div className="flex-1 bg-white p-6 rounded-xl shadow-sm border border-gray-200 w-full relative">
                   <div className="absolute -top-3 -right-3 bg-secondary text-white text-xs font-bold px-3 py-1 rounded-full shadow-md">MERGED</div>
                   <div className="flex items-center mb-4">
                     <svg className="w-5 h-5 text-gray-500 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                     <span className="font-bold text-gray-800">Pull Request #42</span>
                   </div>
                   <div className="space-y-2">
                      <div className="h-2 bg-green-100 rounded w-full"></div>
                      <div className="h-2 bg-green-100 rounded w-5/6"></div>
                      <div className="h-2 bg-green-100 rounded w-4/6"></div>
                   </div>
                 </div>
               </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-base font-semibold tracking-wide text-primary uppercase">Powerful Features</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              Everything you need to automate your feedback loop
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="h-12 w-12 rounded-xl bg-indigo-100 flex items-center justify-center text-primary mb-6">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">One-Click Install</h3>
              <p className="text-gray-500">
                Connect your GitHub repository in seconds. We handle the webhooks and permissions automatically.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow">
               <div className="h-12 w-12 rounded-xl bg-emerald-100 flex items-center justify-center text-secondary mb-6">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Embed Anywhere</h3>
              <p className="text-gray-500">
                A lightweight JavaScript widget that works on React, Vue, Svelte, or plain HTML sites.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow">
               <div className="h-12 w-12 rounded-xl bg-amber-100 flex items-center justify-center text-accent mb-6">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">AI-Powered Triage</h3>
              <p className="text-gray-500">
                Our agent analyzes the feedback, finds the relevant code, and creates a fix for you to review.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center mb-4 md:mb-0">
             <span className="text-xl font-bold text-green-800">feedbackflow</span>
             <span className="ml-4 text-green-800 text-sm">© 2026 feedbackflow Inc.</span>
          </div>
          <div className="flex space-x-6">
            <a href="#" className="text-gray-400 hover:text-gray-600">Privacy</a>
            <a href="#" className="text-gray-400 hover:text-gray-600">Terms</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
