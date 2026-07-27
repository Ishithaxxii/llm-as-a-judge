import { motion } from "framer-motion";

const orbs = [
  { size: 90, x: -140, y: -120, color: "from-primary to-secondary", delay: 0 },
  { size: 70, x: 150, y: -90, color: "from-secondary to-accent", delay: 1 },
  { size: 65, x: -170, y: 110, color: "from-accent to-primary", delay: 2 },
  { size: 85, x: 160, y: 120, color: "from-primary to-accent", delay: 3 },
  { size: 55, x: 0, y: -200, color: "from-secondary to-primary", delay: 4 },
  { size: 60, x: 0, y: 200, color: "from-accent to-secondary", delay: 5 },
];

export default function FloatingConsensus() {
  return (
    <div className="relative flex h-[560px] w-[560px] items-center justify-center">

      {/* Background Glow */}
      <div className="absolute h-[500px] w-[500px] rounded-full bg-primary/10 blur-[120px]" />

      {/* Center Core */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{
          duration: 35,
          repeat: Infinity,
          ease: "linear",
        }}
        className="absolute flex h-48 w-48 items-center justify-center rounded-full border border-white/10 bg-card/40 backdrop-blur-3xl"
      >
        <motion.div
          animate={{
            scale: [1, 1.08, 1],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
          }}
          className="flex h-28 w-28 items-center justify-center rounded-full bg-gradient-to-br from-primary via-secondary to-accent shadow-glow"
        >
          <div className="h-16 w-16 rounded-full bg-background/80 backdrop-blur-xl" />
        </motion.div>
      </motion.div>

      {/* Floating Orbs */}
      {orbs.map((orb) => (
        <motion.div
          key={orb.delay}
          initial={{
            x: orb.x,
            y: orb.y,
          }}
          animate={{
            x: [orb.x, orb.x + 18, orb.x],
            y: [orb.y, orb.y - 22, orb.y],
          }}
          transition={{
            duration: 6 + orb.delay,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute"
        >
          <div
            className={`rounded-full bg-gradient-to-br ${orb.color} opacity-80 blur-sm`}
            style={{
              width: orb.size,
              height: orb.size,
            }}
          />

          <div
            className="absolute inset-2 rounded-full border border-white/20 backdrop-blur-xl"
          />
        </motion.div>
      ))}

      {/* Ambient Particles */}
      {[...Array(18)].map((_, i) => (
        <motion.div
          key={i}
          animate={{
            y: [0, -18, 0],
            opacity: [0.3, 1, 0.3],
          }}
          transition={{
            duration: 3 + Math.random() * 4,
            repeat: Infinity,
          }}
          className="absolute rounded-full bg-white/40"
          style={{
            width: 4 + Math.random() * 4,
            height: 4 + Math.random() * 4,
            left: `${10 + Math.random() * 80}%`,
            top: `${10 + Math.random() * 80}%`,
          }}
        />
      ))}
    </div>
  );
}