const Footer = () => {
    return (
        <footer className="inset-x-0 bottom-[-100%] z-50 flex h-fit w-full justify-center">
            <div className="flex w-full items-start justify-between rounded-t-xl bg-(--bg-transparent) px-6 py-4 backdrop-blur-md">
                <span className="text-sm text-gray-500">
                    © {new Date().getFullYear()} PM Assistant. Все права
                    защищены.
                </span>
            </div>
        </footer>
    )
}

export default Footer
