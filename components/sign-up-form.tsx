"use client";

import { signUpAction } from "@/app/actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Link from "next/link";
import { useCallback, useState } from "react";
import { useFormState } from "react-dom";

/**
 * Password strength levels with visual feedback
 */
interface PasswordStrength {
  level: "weak" | "medium" | "strong";
  feedback: string;
}

/**
 * Calculate password strength based on criteria
 * @param password - Password to evaluate
 * @returns Strength assessment with feedback
 */
function getPasswordStrength(password: string): PasswordStrength {
  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const specialCharPattern = /[!"#$%&'()*+,\-./:;?@[\\\]^_`{|}~]/;
  const hasSpecial = specialCharPattern.test(password);
  const isLongEnough = password.length >= 8;

  if (!isLongEnough) {
    return {
      level: "weak",
      feedback: "Password must be at least 8 characters",
    };
  }

  if (hasUppercase && hasLowercase && hasNumbers && hasSpecial) {
    return { level: "strong", feedback: "Strong password" };
  }

  if ((hasUppercase || hasLowercase) && hasNumbers) {
    return {
      level: "medium",
      feedback: "Medium password - add special characters",
    };
  }

  return {
    level: "weak",
    feedback: "Add uppercase, numbers, and special characters",
  };
}

export function SignUpForm() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [state, formAction] = useFormState(signUpAction, {
    error: "",
    success: false,
  });

  const strength = getPasswordStrength(password);
  const passwordsMatch = password === confirmPassword && password.length > 0;

  const handlePasswordChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setPassword(e.target.value);
    },
    [],
  );

  return (
    <form action=formAction className="space-y-4">
      {state.error && (
        <div
          id="email-error"
          role="alert"
          className="text-sm text-destructive"
        >
          {state.error}
        </div>
      )}

      <div>
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          name="email"
          type="email"
          placeholder="analyst@abaco.finance"
          required
          aria-required="true"
          aria-describedby={state.error ? "email-error" : undefined}
        />
      </div>

      <div>
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          name="password"
          type="password"
          placeholder="••••••••"
          value=password
          onChange=handlePasswordChange
        />
        <div className="mt-2">
          <div className="flex items-center space-x-2">
            <div className="flex-1 bg-gray-200 rounded-full h-2">
              <div
                className={`h-full transition-all ${
                  strength.level === "weak"
                    ? "w-1/3 bg-red-500"
                    : strength.level === "medium"
                    ? "w-2/3 bg-yellow-500"
                    : "w-full bg-green-500"
                }`}
              />
            </div>
            <span className="text-sm capitalize">{strength.level}</span>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            {strength.feedback}
          </p>
        </div>
      </div>

      <div>
        <Label htmlFor="confirmPassword">Confirm Password</Label>
        <Input
          id="confirmPassword"
          name="confirmPassword"
          type="password"
          value=confirmPassword
          onChange={(e) => setConfirmPassword(e.target.value)}
          aria-describedby={!passwordsMatch ? "password-mismatch" : undefined}
        />
        {!passwordsMatch && password.length > 0 && (
          <p
            id="password-mismatch"
            role="status"
            aria-live="polite"
            className="text-xs text-destructive mt-1"
          >
            Passwords do not match
          </p>
        )}
      </div>

      <Button type="submit" className="w-full" disabled={!passwordsMatch}>
        Sign Up
      </Button>

      <p className="text-center text-sm text-muted-foreground">
        Already have an account?{" "}
        <Link href="/auth/sign-up" className="text-primary hover:underline">
          Log in
        </Link>
      </p>
    </form>
  );
}