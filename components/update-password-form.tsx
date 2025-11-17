"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export default function UpdatePasswordForm() {
  const [newPassword, setNewPassword]  useState("");
  const [confirmPassword, setConfirmPassword]  useState("");
  const [state, setState]  useState({ error: null });

  const handleSubmit  async (e: React.FormEvent)  {
    e.preventDefault();
    if (newPassword ! confirmPassword) {
      setState({ error: "Passwords do not match" });
      return;
    }
    // Handle password update logic here
  };

  return (
    form onSubmithandleSubmit className"space-y-4"
      div
        Label htmlFor"new-password"New password/Label
        Input
          id"new-password"
          type"password"
          valuenewPassword
          onChange{(e: React.ChangeEventHTMLInputElement)  setNewPassword(e.target.value)}
          required
        /
      /div
      
        Label htmlFor"confirm-password"Confirm password/Label
          id"confirm-password"
          valueconfirmPassword
          onChange{(e: React.ChangeEventHTMLInputElement)  setConfirmPassword(e.target.value)}

      {newPassword && confirmPassword && newPassword ! confirmPassword && (
        p className"text-red-500 text-sm"Passwords do not match/p
      )}

      Button type"submit" disabled{!newPassword || !confirmPassword}
        Reset password
      /Button
      
      {state.error && p className"text-red-500 text-sm"{state.error}/p}
    /form
  );
}
