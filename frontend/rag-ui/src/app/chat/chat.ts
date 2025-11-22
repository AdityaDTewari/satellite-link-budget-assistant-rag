import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Api } from '../services/api';
import { Message } from '../models/message';
import { v4 as uuidv4 } from 'uuid';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    HttpClientModule
  ],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class Chat {
  messages: Message[] = [];
  input = '';
  loading = false;
  topK = 4;

  constructor(private api: Api) {
    // Optional: a system message to set context in the UI
    // this.messages.push({
    //   id: this._makeId(),
    //   role: 'system',
    //   text: 'Link Budget Assistant — ask a SATCOM question (e.g., "Compute FSPL at 12 GHz for GEO")',
    //   time: new Date().toISOString()
    // });
  }

  private _makeId() {
    try {
      return uuidv4();
    } catch {
      return String(Date.now());
    }
  }

  send() {
    const text = this.input.trim();
    if (!text) return;

    const userMsg: Message = {
      id: this._makeId(),
      role: 'user',
      text,
      time: new Date().toISOString()
    };

    this.messages.push(userMsg);
    this.input = '';
    this.loading = true;

    this.api.sendQuery(text, this.topK).subscribe({
      next: (res) => {
        const assistantMsg: Message = {
          id: this._makeId(),
          role: 'assistant',
          text: res.answer,
          time: new Date().toISOString()
        };
        this.messages.push(assistantMsg);
        this.loading = false;
      },
      error: (err) => {
        const errMsg: Message = {
          id: this._makeId(),
          role: 'system',
          text: `[ERROR] Could not reach backend. ${err?.message || ''}`,
          time: new Date().toISOString()
        };
        this.messages.push(errMsg);
        this.loading = false;
      }
    });
  }

  isUser(m: Message) { return m.role === 'user'; }
  isAssistant(m: Message) {return m.role === 'assistant'; }
  isSystem(m: Message) {return m.role === 'system'; }
}
