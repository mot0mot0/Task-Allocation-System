import { Link } from "react-router-dom"

const Navbar = () => {
    return (
        <div className="fixed inset-x-0 top-0 z-50">
            <div className="flex items-center justify-between rounded-b-xl bg-white px-6 py-2 shadow-md">
                <Link to="/" className="no-underline">
                    <div className="flex items-center">
                        <i className="pi pi-tasks mr-2 text-3xl text-[#72efdd]"></i>
                        <span className="text-2xl font-bold text-[#72efdd]">
                            PM Assistant
                        </span>
                    </div>
                </Link>
                <div className="flex gap-6">
                    <Link
                        to="/docs"
                        className="flex items-center rounded-lg px-4 py-2 text-[#64748b] transition-all duration-300 hover:bg-[#f8fafc] hover:text-[#72efdd]"
                    >
                        <i className="pi pi-fw pi-file mr-2 text-lg"></i>
                        <span className="text-lg">Docs</span>
                    </Link>
                    <Link
                        to="/demo"
                        className="flex items-center rounded-lg px-4 py-2 text-[#64748b] transition-all duration-300 hover:bg-[#f8fafc] hover:text-[#72efdd]"
                    >
                        <i className="pi pi-fw pi-play mr-2 text-lg"></i>
                        <span className="text-lg">Demo</span>
                    </Link>
                </div>
            </div>
        </div>
    )
}

export default Navbar
