## JS/TS Style
- Use TypeScript 5.x in `strict` mode with `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, and `useDefineForClassFields`. Model external contracts with dedicated `.d.ts` or `zod` schemas.
- Adopt ESLint flat config with `@typescript-eslint` recommended rules, `eslint-plugin-import`, `eslint-plugin-unicorn`, and SonarJS for bug traps. Keep autofixers (`eslint --fix`) in CI.
- Format with Prettier 3 (`printWidth: 100`, `trailingComma: "all"`, `singleQuote: true`) and rely on Prettier for stylistic concerns, leaving logic checks to ESLint.
- Prefer immutable data patterns, pure functions, `const` over `let`, and narrow union types early. Guard async flows with `await` + error boundaries and always handle rejected promises.
- Structure modules using ECMAScript modules, export minimal public surfaces, and avoid default exports except for frameworks that require them.
- Tests: use Vitest/Jest with `@testing-library` for UI, enforce coverage thresholds, and stub network IO via MSW or similar.
