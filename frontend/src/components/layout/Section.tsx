import { type SectionProps } from "../../types/section";
import { Container } from "./Container";
import Reveal from "../common/Reveal";

export const Section = ({ id, children, className }: SectionProps) => {
    return (
        <Reveal>
            <section className={`py-12 ${className || ""}`} id={id}>
                <Container>{children}</Container>
            </section>
        </Reveal>
    );
};
