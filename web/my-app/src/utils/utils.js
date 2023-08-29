export function getOrDefault(val, defaultVal) {
    if (val === undefined) {
        return defaultVal;
    }

    return val;
}