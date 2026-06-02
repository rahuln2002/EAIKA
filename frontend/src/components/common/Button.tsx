import { type ButtonProps } from "../../types/button";

export const Button = ({ label, url, newTab = true }: ButtonProps) => {
    return (
        <a
            href={url}
            target={newTab ? "_blank" : "_self"}
            rel="noopener noreferrer"
            className="
                inline-block
                bg-gray-900/80 hover:bg-blue-500/80
                backdrop-blur-lg
                text-white
                font-bold
                py-2 px-4
                rounded-2xl
                cursor-pointer
                transition-all duration-300
                border border-white/20
                shadow-lg
                hover:scale-105
                mr-2
            "
        >
            {label}
        </a>
    );
};
