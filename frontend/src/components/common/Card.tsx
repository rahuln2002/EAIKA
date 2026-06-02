import { type CardProps } from "../../types/card";

export const Card = ({
    title,
    description,
    image,
    children,
    className = "",
}: CardProps) => {
    return (
        <div
            className={`
                rounded-2xl
                border
                border-gray-700
                p-6
                ${className}
            `}
        >
            {image && (
                <img
                    src={image}
                    alt={title || "Card Image"}
                    className="
                        w-full
                        h-48
                        object-cover
                        rounded-xl
                        mb-4
                    "
                />
            )}

            {title && (
                <h3
                    className="
                        text-2xl
                        font-bold
                        mb-2
                    "
                >
                    {title}
                </h3>
            )}

            {description && (
                <p
                    className="
                        leading-relaxed
                        p-2
                        text-justify
                    "
                >
                    {description.map((line, index) => (
                        <li key={index}>{line}</li>
                    ))}
                </p>
            )}

            {children}
        </div>
    );
};
