import { Routes } from '@angular/router';
import { Chat } from './chat/chat';

export const routes: Routes = [
    {
        path: '', title: 'RAG Chat', component: Chat
    },
    {
        path: '**', redirectTo: ''
    }
];
