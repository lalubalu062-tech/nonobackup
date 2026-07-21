export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white">

      {/* Top Advertisement */}
      <section className="bg-white text-gray-900 mx-4 mt-4 p-6 rounded-xl text-center shadow">
        <h3 className="text-xl font-bold">
          Advertisement
        </h3>
        <p className="text-gray-600">
          Your Ads Here
        </p>
      </section>


      {/* Navbar */}
      <nav className="flex justify-between items-center px-8 py-6">

        <h1 className="text-3xl font-bold text-sky-400">
          NONO HUB
        </h1>

        <div>
          <button className="mr-5 text-white font-semibold">
            Login
          </button>

          <button className="bg-sky-500 hover:bg-sky-600 px-6 py-3 rounded-lg font-bold">
            Deploy Now
          </button>
        </div>

      </nav>



      {/* Hero */}
      <section className="text-center px-6 py-20">

        <h2 className="text-5xl font-bold">
          Deploy. Run. Scale.
        </h2>

        <p className="mt-6 text-xl text-gray-300 max-w-3xl mx-auto">
          NONO HUB is a free cloud platform where developers
          can deploy, run and monitor applications easily.
        </p>


        <div className="mt-8">

          <button className="bg-sky-500 px-8 py-4 rounded-xl text-lg font-bold">
            Start Building
          </button>

        </div>

      </section>




      {/* Features */}
      <section className="grid md:grid-cols-3 gap-6 px-8">


        <div className="bg-slate-900 border border-slate-700 p-6 rounded-xl">

          <h3 className="text-2xl font-bold text-sky-400">
            🚀 Easy Deployment
          </h3>

          <p className="mt-3 text-gray-300">
            Deploy your Python, Node.js and web applications
            from GitHub or local projects.
          </p>

        </div>



        <div className="bg-slate-900 border border-slate-700 p-6 rounded-xl">

          <h3 className="text-2xl font-bold text-sky-400">
            ⚡ Auto Recovery
          </h3>

          <p className="mt-3 text-gray-300">
            Your services can automatically restart
            when stopped or crashed.
          </p>

        </div>



        <div className="bg-slate-900 border border-slate-700 p-6 rounded-xl">

          <h3 className="text-2xl font-bold text-sky-400">
            📊 Live Monitoring
          </h3>

          <p className="mt-3 text-gray-300">
            Monitor RAM, CPU usage and project status
            in real time.
          </p>

        </div>


      </section>




      {/* User Can Use */}
      <section className="px-8 py-16">

        <h2 className="text-4xl font-bold text-center">
          What You Can Build With NONO HUB
        </h2>


        <div className="grid md:grid-cols-2 gap-6 mt-10">


          <div className="bg-slate-900 p-6 rounded-xl">

            <h3 className="text-xl font-bold text-sky-400">
              Web Applications
            </h3>

            <p className="text-gray-300 mt-2">
              Host websites, APIs and backend services.
            </p>

          </div>



          <div className="bg-slate-900 p-6 rounded-xl">

            <h3 className="text-xl font-bold text-sky-400">
              Automation Tools
            </h3>

            <p className="text-gray-300 mt-2">
              Run scripts, bots and scheduled tasks.
            </p>

          </div>



          <div className="bg-slate-900 p-6 rounded-xl">

            <h3 className="text-xl font-bold text-sky-400">
              Developer Testing
            </h3>

            <p className="text-gray-300 mt-2">
              Test projects without managing servers.
            </p>

          </div>



          <div className="bg-slate-900 p-6 rounded-xl">

            <h3 className="text-xl font-bold text-sky-400">
              Cloud Projects
            </h3>

            <p className="text-gray-300 mt-2">
              Deploy and manage multiple applications.
            </p>

          </div>


        </div>

      </section>





      {/* How it Works */}
      <section className="text-center px-8 py-12">

        <h2 className="text-4xl font-bold">
          How NONO HUB Works
        </h2>

        <p className="text-gray-300 mt-5">
          1. Create account
          <br/>
          2. Upload or connect project
          <br/>
          3. Deploy application
          <br/>
          4. Monitor resources
        </p>

      </section>




      {/* Footer */}
      <footer className="bg-sky-600 text-center p-6 mt-10">

        <h3 className="font-bold text-xl">
          NONO HUB
        </h3>

        <p>
          Free Cloud Platform For Developers
        </p>

        <p className="mt-3">
          © 2026 NONO HUB
        </p>

      </footer>


    </main>
  );
}
