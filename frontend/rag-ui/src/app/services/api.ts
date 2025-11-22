import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

interface BackendQuery {
  question: string;
  top_k?: number;
}

interface BackendResponse {
  answer: string;
}

@Injectable({
  providedIn: 'root',
})
export class Api {
  private base = environment.apiBase;

  constructor(private http: HttpClient) {}

  /**
   * sendQuery
   * @param question user question string
   * @param top_k how many docs to retrieve (optional)
   * @returns Observable of backend response
   */
  sendQuery(question: string, top_k = 4): Observable<BackendResponse> {
    const payload: BackendQuery = { question, top_k };

    return this.http.post<BackendResponse>(`${this.base}/query`, payload);
  }
}
