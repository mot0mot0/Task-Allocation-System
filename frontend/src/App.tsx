import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Navbar from "./components/Navbar"
import Home from "./pages/Home"
import Demo from "./pages/Demo"
import Docs from "./pages/Docs"
import "primereact/resources/themes/lara-light-indigo/theme.css"
import "primereact/resources/primereact.min.css"
import "primeicons/primeicons.css"

function App() {
    return (
        <Router>
            <div className="h-full w-full">
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/demo" element={<Demo />} />
                    <Route path="/docs" element={<Docs />} />
                </Routes>
            </div>
        </Router>
    )
}

export default App
