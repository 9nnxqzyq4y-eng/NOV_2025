import TutorialStep from "./tutorial-step";

export default function SignUpUserSteps() {
  return (
    <>
      <TutorialStep title="Sign up your first user">
        Run <code>npm run dev</code> and open the app at{" "}
        <a href="http://localhost:3000" target="_blank" rel="noopener noreferrer">
          localhost:3000
        </a>
        . Use the sign-up form to create an operator account with your corporate
        email domain.
      </TutorialStep>
      
      <TutorialStep title="Verify email">
        Verify the confirmation email sent by Supabase and sign in.
      
      <TutorialStep title="Assign admin role">
        Assign admin role via Supabase Auth &rarr; Users to
        unlock analytics administration features.
      
      <TutorialStep title="Continue implementation">
        Continue with the ABACO_IMPLEMENTATION_SUMMARY.md{" "}
        milestone checklist to configure provider credentials, deploy to Cloud
        Run, and schedule the nightly ingestion job.
    </>
  );
}
