package com.resy

import com.resy.BookingDetails.{time, _}
import com.resy.ResyApiWrapper._
import org.joda.time.DateTime
import play.api.libs.json.JsResult.Exception
import play.api.libs.json.{JsArray, JsError, Json}

import scala.annotation.tailrec
import scala.concurrent.duration._
import scala.concurrent.{Await, Future}
import scala.util.{Failure, Success, Try}
import scala.util.Random 

object BookReservationWorkflow {
  implicit val testing = false

  /**
    * STEP 1: FIND RESERVATION (GET CONFIG ID)
    * @return
    */
  private[this] def findReservation: Future[String] = {
    val findResQueryParams = Map(
      "day" -> day,
      "lat" -> "0",
      "long" -> "0",
      "party_size" -> partySize,
      "venue_id" -> venueId)
    sendGetRequest(ResyApiMapKeys.FindReservation, findResQueryParams)
  }

  /**
    * STEP 2: GET RESERVATION DETAILS (GET PAYMENT ID AND BOOK TOKEN)
    * @param configId
    * @return
    */
  def getReservationDetails(configId: String) = {
    val findResQueryParams = Map(
      "config_id" -> configId,
      "day" -> day,
      "party_size" -> partySize)

    sendGetRequest(ResyApiMapKeys.ReservationDetails, findResQueryParams)
  }

  /**
    * STEP 3: BOOK RESERVATION
    * @param resDetailsResp
    * @return
    */
  def bookReservation(resDetailsResp: String) = {
    val resDetails = Json.parse(resDetailsResp)
    println(s"${DateTime.now} URL Response: $resDetailsResp")

    //PaymentMethodId - Searching for this pattern - "payment_methods": [{"is_default": true, "provider_name": "braintree", "id": 123456, "display": "1234", "provider_id": 1}]
    val paymentMethodId = "Nothing"
      //(resDetails \ "user" \ "payment_methods" \ 0 \ "id")
        //.get
        //.toString

    println(s"${DateTime.now} Payment Method Id: $paymentMethodId")

    //BookToken - Searching for this pattern - "book_token": {"value": "book_token_value"
    val bookToken =
      (resDetails \ "book_token" \ "value")
        .get
        .toString
        .stripPrefix("\"")
        .stripSuffix("\"")

    println(s"${DateTime.now} Book Token: $bookToken")

    val bookResQueryParams = Map(
      "book_token" -> bookToken,
      //"struct_payment_method" -> s"""{"id":$paymentMethodId}""",
      "source_id" -> "resy.com-venue-details")

    sendPostRequest(ResyApiMapKeys.BookReservation, bookResQueryParams)
  }

  /**
    * Same as Step 1 but does a retry.  Blocks because the reservation can't proceed without an available reservation
    * @param endTime
    * @return
    */
  @tailrec
  def retryFindReservation(endTime: Long): String = {
    val findResResp = Await.result(findReservation, 5 seconds)

    println(s"${DateTime.now} URL Response: $findResResp")
  
    val reservations_available = Try(((Json.parse(findResResp) \ "results" \ "venues" \ 0 \ "slots")
        .get
        .as[JsArray]
        .value
        .filter(x => time.contains((x \ "date" \ "start").get.toString)).length))
    println(s"reservations_available: $reservations_available")
    reservations_available match {
      case Success(reservations_available) =>
        val num_res = reservations_available
        val reservation =
        ((Json.parse(findResResp) \ "results" \ "venues" \ 0 \ "slots")
        .get
        .as[JsArray]
        .value
        .filter(x => time.contains((x \ "date" \ "start").get.toString))
        (Random.nextInt(num_res)) \ "config" \ "token")
        .get
        .toString
        println(s"reservations_available: $reservations_available")
        println(s"${DateTime.now} Config Id: $reservation")
        val reservation_short = reservation.substring(1, reservation.length() - 1)
        reservation_short
      case Failure(_) if endTime - DateTime.now.getMillis > 0 =>
        retryFindReservation(endTime)
      case _ =>
        throw new Exception(JsError("Could not find a reservation for the given time"))
    }


    //println(s"There were $reservations_available that satisfied the constraints")
    //ConfigId - Searching for this pattern - "time_slot": "17:15:00", "badge": null, "service_type_id": 2, "colors": {"background": "2E6D81", "font": "FFFFFF"}, "template": null, "id": 123457
    

    // reservation match {
    //   case Success(configId) =>
    //     println(s"${DateTime.now} Config Id: $configId")
    //     configId
    //   case Failure(_) if endTime - DateTime.now.getMillis > 0 =>
    //     retryFindReservation(endTime)
    //   case _ =>
    //     throw new Exception(JsError("Could not find a reservation for the given time"))
    // }
  }
}