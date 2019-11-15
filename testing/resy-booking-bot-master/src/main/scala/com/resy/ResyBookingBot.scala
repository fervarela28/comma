package com.resy

import akka.actor.ActorSystem
import com.resy.BookReservationWorkflow._
import org.joda.time.DateTime
import play.api.libs.json._

import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.duration._
import scala.util.{Failure, Success, Try}

object ResyBookingBot {
  def main(args: Array[String]): Unit = {
    println("Starting Resy Booking Bot")
    val user_key = BookingDetails.users get args(0)
    BookingDetails.auth_token = user_key.get
    BookingDetails.venueId = args(1)
    BookingDetails.partySize = args(2)
    val days_in_the_future = BookingDetails.days_from_today.getOrElse(args(1), 1)
    BookingDetails.day = DateTime.now.plusDays(days_in_the_future).toString("yyyy-MM-dd")
    val system = ActorSystem("System")
    val startOfTomorrow = DateTime.now.withTimeAtStartOfDay.plusDays(1).getMillis
    val millisUntilTomorrow = startOfTomorrow - DateTime.now.getMillis
    val hoursRemaining = millisUntilTomorrow/1000/60/60
    val minutesRemaining = millisUntilTomorrow/1000/60 - hoursRemaining * 60
    val secondsRemaining = millisUntilTomorrow/1000 - hoursRemaining * 60 * 60 - minutesRemaining * 60

    println(s"Current time: ${DateTime.now}")
    println(s"Sleeping for $hoursRemaining hours, $minutesRemaining minutes and $secondsRemaining seconds")
    println(millisUntilTomorrow - 10000)
    system.scheduler.scheduleOnce(millisUntilTomorrow - 10000 millis)(bookReservationWorkflow)
  }

  def bookReservationWorkflow = {
    println(s"Attempting to snipe reservation at ${DateTime.now}")

    //Try to get configId of the time slot for 10 seconds
    val findResResp = retryFindReservation(DateTime.now.plusSeconds(13).getMillis)
    println(s"Succeeded at finding reservation")
    //Try to book the reservation
    for(resDetailsResp <- getReservationDetails(findResResp);
        bookResResp <- bookReservation(resDetailsResp)
    ) {
      val resyToken =
        Try((Json.parse(bookResResp) \ "resy_token")
          .get
          .toString
          .stripPrefix("\"")
          .stripSuffix("\"")
        )

      resyToken match {
        case Success(token) =>
          println(s"Successfully sniped reservation at ${DateTime.now}")
          println(s"Resy token is $token")
        case Failure(error) =>
          println(s"Couldn't sniped reservation at ${DateTime.now}")
          println(s"Error message is $error")
      }

      println("Shutting down Resy Booking Bot at " + DateTime.now)
      System.exit(0)
    }
  }
}
