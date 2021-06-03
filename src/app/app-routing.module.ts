import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ChannelsComponent } from './channels/channels.component';
import { HomeComponent } from './home/home.component';
import { VideosComponent } from './videos/videos.component';

const routes: Routes = [
  //{ path: '', component: HomeComponent },
  //{ path: 'channel', redirectTo: ''},
  { path: '', component: ChannelsComponent },
  { path: 'video', redirectTo: ''},
  { path: 'video/:id', component: VideosComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
