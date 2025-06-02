import { Link } from "react-router-dom"

const Navbar = () => {
    return (
        <div className="fixed inset-x-0 top-0 z-50 flex justify-center">
            <div className="mx-5 flex w-full max-w-[1024px] items-center justify-between rounded-b-xl bg-(--bg-transparent) px-6 py-2 backdrop-blur-md">
                <Link to="/" className="no-underline">
                    <div className="flex items-center rounded-lg px-3 py-1 transition-colors duration-300 hover:bg-(--bg-transparent-hover)">
                        <span className="text-2xl font-bold text-(--primary-app-color)">
                            PM Assistant
                        </span>
                    </div>
                </Link>
                <div className="flex gap-2">
                    <Link
                        to="/docs"
                        className="flex items-center rounded-lg px-4 py-2 text-[#64748b] transition-all duration-300 hover:bg-(--bg-transparent-hover) hover:text-(--primary-app-color)"
                    >
                        <i className="pi pi-fw pi-file mr-2 text-lg"></i>
                        <span className="text-lg">Docs</span>
                    </Link>
                    <Link
                        to="/demo"
                        className="flex items-center rounded-lg px-4 py-2 text-[#64748b] transition-all duration-300 hover:bg-(--bg-transparent-hover) hover:text-(--primary-app-color)"
                    >
                        <i className="pi pi-fw pi-play mr-2 text-lg"></i>
                        <span className="text-lg">Demo</span>
                    </Link>
                    <div className="flex">
                        <a
                            href="https://github.com/mot0mot0/Task-Allocation-System"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center rounded-lg p-2 text-[#64748b] transition-all duration-300 hover:bg-(--bg-transparent-hover) hover:text-(--primary-app-color)"
                        >
                            <i
                                className="pi pi-github"
                                style={{ fontSize: "1.4rem" }}
                            ></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Navbar
