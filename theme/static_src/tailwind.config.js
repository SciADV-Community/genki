module.exports = {
    content: ["../../terminal/templates/**/*.html", "../../genki/templates/**/*.html"],
    theme: {
        extend: {
            screens: {
                dark: { raw: "(prefers-color-scheme: dark)" },
            },
        },
    },
    plugins: [
        require("@tailwindcss/forms"),
        require("@tailwindcss/typography"),
        require("@tailwindcss/line-clamp"),
        require("@tailwindcss/aspect-ratio"),
    ],
};
