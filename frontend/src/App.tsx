import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar/ui/Navbar"
import HomePage from "./pages/Home"
import DemoPage from "./pages/Demo"
import DocsPage from "./pages/Docs/ui/DocsPage"
import "primereact/resources/themes/lara-light-indigo/theme.css"
import "primereact/resources/primereact.min.css"
import "primeicons/primeicons.css"
import AppBackground from "./components/AppBackground"
import Footer from "./components/Footer"

function App() {
    return (
        <Router>
            <div className="m-[0px] flex h-full w-full flex-col items-center justify-center">
                <AppBackground />
                <Navbar />
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/demo" element={<DemoPage />} />
                    <Route path="/docs" element={<DocsPage />} />
                </Routes>
                <Footer />
            </div>
        </Router>
    )
}

export default App
