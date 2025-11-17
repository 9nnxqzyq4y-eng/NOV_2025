import { Checkbox } from "@/components/ui/checkbox";

interface TutorialStepProps {
  title: string;
  children: React.ReactNode;
}

export default function TutorialStep({ title, children }: TutorialStepProps) {
  return (
    div className"flex gap-3 my-6"
      Checkbox idtitle /
      label htmlFortitle className"text-sm"
        div className"font-medium mb-1"title/div
        div className"text-muted-foreground"children/div
      /label
    /div
  );
