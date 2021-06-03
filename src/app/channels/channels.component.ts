import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DataService } from '../data.service';
import { MatTabChangeEvent } from '@angular/material/tabs';

@Component({
  selector: 'app-channels',
  templateUrl: './channels.component.html',
  styleUrls: ['./channels.component.scss']
})
export class ChannelsComponent implements OnInit {
  channel_name;
  channel_data;
  videos = [];
  games = [];
  breakpoint = 5;
  breakpoint_game = 6;
  
  constructor(private route: ActivatedRoute, private dataService: DataService) { }

  ngOnInit(): void {
    this.channel_name = this.route.snapshot.params['name'];
    this.channel_name = 'jakenbakeLIVE';

    this.dataService.getChannels().subscribe((data: any[]) => {
      data.forEach(currentChannel => {
        if (currentChannel.name.toLowerCase() === this.channel_name.toLowerCase()) {
          this.channel_data = currentChannel;
          console.log(currentChannel);
        }
      });
    });

    this.dataService.getVideo(this.channel_name, 50, 0).subscribe((data: any[]) => {
      this.videos = data;
    });

    this.setBreakpoint();
  }

  onPageChange(event) {
    this.videos = [];
    this.dataService.getVideo(this.channel_name, event.pageSize, event.pageIndex * event.pageSize).subscribe((data: any[]) => {
      this.videos = data;
    });
  }

  onResize(event) {
    this.setBreakpoint();
  }

  setBreakpoint()
  {
    this.breakpoint = window.innerWidth / 400;
    this.breakpoint_game = window.innerWidth / 280;
  }

  tabChanged(tabChangeEvent: MatTabChangeEvent): void {
    if (tabChangeEvent.index == 1 && this.games.length == 0) {
      this.dataService.getGameList(this.channel_name).subscribe((data: any[]) => {
        this.games = data;
      });
    }
  }

  sortBy(prop: string) {
      return this.videos.sort((a, b) => a[prop] < b[prop] ? 1 : a[prop] === b[prop] ? 0 : -1);
  }
}

