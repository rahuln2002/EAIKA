import { motion } from "framer-motion";

type RevealProps = {
    children: React.ReactNode;
};

export default function Reveal({ children }: RevealProps) {
    return (
        <motion.div
            initial={{
                opacity: 0,
                x: -80,
                y: 80,
            }}
            whileInView={{
                opacity: 1,
                x: 0,
                y: 0,
            }}
            viewport={{
                amount: 0.15,
            }}
            transition={{
                duration: 0.6,
                ease: "easeOut",
            }}
        >
            {children}
        </motion.div>
    );
}
