# Security Checklist

## Environment Variables

- ✅ **Never commit `.env.local`** - Add to `.gitignore`
- ✅ **Validate env vars on startup** - Check required variables before app initializes
- ✅ **Use strong API keys** - Generate new keys for each environment (dev, staging, prod)
- ✅ **Rotate secrets regularly** - Update API keys and tokens quarterly

## Docker Security

- ✅ **Never bake secrets into images** - Use Docker secrets, environment variables, or secret management tools
- ✅ **Use non-root user** - Run container as unprivileged user (default: `nextjs:nodejs`)
- ✅ **Use Alpine Linux** - Smaller attack surface
- ✅ **Multi-stage builds** - Keep dev dependencies out of production

## Cookie Security

- ✅ **Validate cookie options** - Only set valid cookie attributes (secure, httpOnly, sameSite)
- ✅ **Handle auth errors** - Catch and log auth failures gracefully
- ✅ **Use HTTPS in production** - Enforce secure cookies

## Database Security

- ✅ **Enable Row Level Security (RLS)** in Supabase
- ✅ **Use parameterized queries** - Prevent SQL injection
- ✅ **Validate all user input** - Both client and server-side

## Deployment

- ✅ **Use environment variables for secrets** - Vercel, Railway, etc.
- ✅ **Enable CORS properly** - Restrict to known domains
- ✅ **Set up security headers** - CSP, X-Frame-Options, etc.

