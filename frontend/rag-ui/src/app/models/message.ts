export interface Message {
    id?: string;
    role: 'user' | 'assistant' | 'system';
    text: string;
    time?: string;
}