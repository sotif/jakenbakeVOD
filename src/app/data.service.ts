import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { shareReplay } from 'rxjs/operators';
import { Observable } from 'rxjs/internal/Observable';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private REST_API_SERVER = "./assets/";
  data$: Observable<Object>;

  constructor(private httpClient: HttpClient) { 
    this.data$ = this.httpClient.get(this.REST_API_SERVER + "channels.json").pipe(shareReplay(1));
  }

  public getChannels() {
    return this.data$;
  }

  public getVideo(channelName: string, limit: number, offset: number) {
    return this.httpClient.get(this.REST_API_SERVER + "videos/" + channelName + ".json");
  }

  public getVideoByGame(channelName: string, gameName: string, limit: number, offset: number) {
    return this.httpClient.get(this.REST_API_SERVER + "/videos?channel_name=" + channelName + "&game=" + encodeURIComponent(gameName) + "&offset=" + offset + "&limit=" + limit);
  }

  public getGameList(channelName: string) {
    return this.httpClient.get(this.REST_API_SERVER + "/games?channel=" + channelName);
  }

  public getVideoById(id: number) {
    return this.httpClient.get(this.REST_API_SERVER + "video/" + id + ".json");
  }

  public sendEmail(form_name: string, form_email: string, form_message: string) {
    return this.httpClient.post("https://twitcharchives.com/api/contact.php", JSON.stringify({name: form_name, email: form_email, message: form_message}));
  }
}
