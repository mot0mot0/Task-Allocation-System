import "../styles/AppBackground.scss"

const AppBackground = () => {
    const BUBBLE_COUNT = 5

    return (
        <div className="fixed top-0 left-0 z-[-1] h-screen w-screen">
            <div className="bubbles">
                {Array.from({ length: BUBBLE_COUNT }).map((_, i) => (
                    <div key={i} className="bubble" />
                ))}
            </div>
            <div className="blur-effect"></div>
        </div>
    )
}

export default AppBackground
