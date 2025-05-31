/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: "#72efdd",
                    light: "#a3ffe8",
                    dark: "#4dffc9",
                },
                background: {
                    DEFAULT: "#f9fafb",
                    dark: "#f3f4f6",
                },
            },
        },
    },
    plugins: [],
}
