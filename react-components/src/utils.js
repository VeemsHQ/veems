export const truncate = (input, max) => (input.length > max ? `${input.substring(0, max + 1)}...` : input);

export const valueOrEmpty = (value) => ((value !== undefined && value !== null) ? value : '');
