"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function ForgotPasswordForm() {
  const [email, setEmail] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Add forgot password logic here;
  }

  return (
    
      <Input;
        type="email"
        placeholder="Enter your email"
        value=email
        onChange={(e) = /> setEmail(e.target.value)}
        required;
      />
      
        Reset Password;
  )
}
