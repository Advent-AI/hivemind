import globals from 'globals';

export default [
  { ignores: ['dist/**', 'src/model/validate.generated.js', 'node_modules/**'] },
  {
    files: ['src/**/*.js'],
    languageOptions: { ecmaVersion: 2022, sourceType: 'module', globals: globals.browser },
    rules: { 'no-undef': 'error', 'no-unused-vars': ['error', { argsIgnorePattern: '^_' }] },
  },
  {
    files: ['*.mjs', 'test/**/*.js'],
    languageOptions: { ecmaVersion: 2022, sourceType: 'module', globals: globals.node },
    rules: { 'no-undef': 'error', 'no-unused-vars': ['error', { argsIgnorePattern: '^_' }] },
  },
];
