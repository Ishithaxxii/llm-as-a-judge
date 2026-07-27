/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#060816",
        surface: "#101828",
        card: "#161B2E",

        primary: "#7C5CFC",
        secondary: "#3B82F6",
        accent: "#22D3EE",

        success: "#22C55E",
        warning: "#F59E0B",
        danger: "#EF4444",

        text: "#F8FAFC",
        muted: "#94A3B8",
      },

      fontFamily: {
        heading: ["Space Grotesk", "sans-serif"],
        body: ["Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },

      borderRadius: {
        xl2: "24px",
      },

      boxShadow: {
        glass: "0 10px 40px rgba(0,0,0,0.35)",
        glow: "0 0 40px rgba(124,92,252,.35)",
      },

      backgroundImage: {
        hero:
          "radial-gradient(circle at top left,#3d2a9a 0%,transparent 35%), radial-gradient(circle at bottom right,#006eff 0%,transparent 35%)",
      },

      keyframes: {
        float: {
          "0%,100%": {
            transform: "translateY(0px)",
          },
          "50%": {
            transform: "translateY(-12px)",
          },
        },

        pulseGlow: {
          "0%,100%": {
            opacity: "0.5",
          },
          "50%": {
            opacity: "1",
          },
        },

        fadeUp: {
          from: {
            opacity: "0",
            transform: "translateY(30px)",
          },
          to: {
            opacity: "1",
            transform: "translateY(0px)",
          },
        },
      },

      animation: {
        float: "float 6s ease-in-out infinite",
        pulseGlow: "pulseGlow 3s ease-in-out infinite",
        fadeUp: "fadeUp .8s ease forwards",
      },
    },
  },
  plugins: [],
};