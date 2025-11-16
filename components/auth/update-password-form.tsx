"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function UpdatePasswordForm() {
  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Add update password logic here;
  }

  return (
    
      <Input;
        type="password"
        placeholder="New password"
        value=newPassword
        onChange={(e) = /> setNewPassword(e.target.value)}
        required;
      />
        placeholder="Confirm password"
        value=confirmPassword
        onChange={(e) = /> setConfirmPassword(e.target.value)}
      
        Update Password;
  )
}
