"use client";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Laptop, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

const ThemeSwitcher  ()  {
  const [mounted, setMounted]  useState(false);
  const { theme, setTheme }  useTheme();

  // useEffect only runs on the client, so now we can safely show the UI useEffect(()  {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  const ICON_SIZE  16;

  return (
    
          {theme  "light" ? (
            Sun;
              key"light"
              sizeICON_SIZE
              className{"text-muted-foreground"}
            /
          ) : theme  "dark" ? (
            Moon;
              key"dark"
          ) : (
            Laptop;
              key"system"
          )}
        
        DropdownMenuRadioGroup;
          valuetheme
          onValueChange{(value: string)  / setTheme(value)}
        
          
            {" "}
            Light;
            Dark;
            System;
  );
};

export { ThemeSwitcher };
